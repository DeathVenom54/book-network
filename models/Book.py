import json
import urllib.parse

import requests
from models.Database import Database

class BookData:
    def __init__(self, work_id, title, author, description, cover, subjects):
        self.work_id = work_id
        self.title = title
        self.author = author
        self.description = description
        self.cover = cover
        self.subjects = subjects

    def __str__(self):
        return f'{self.work_id}: {self.title} - {self.author}'

    @staticmethod
    def from_work_id(work_id):
        try:
            # check in database first
            db = Database()
            cursor = db.db.cursor()
            cursor.execute('SELECT title, author, description, cover, subjects FROM book_data WHERE work_id = %s;', (work_id,))
            db_book_data = cursor.fetchone()
            if db_book_data:
                return BookData(work_id, db_book_data[0], db_book_data[1], db_book_data[2], db_book_data[3], json.loads(db_book_data[4]))

            # fetch from openlibrary api
            res = requests.get(f'https://openlibrary.org/works/{work_id}.json')
            if res.status_code != 200:
                return None
            book_data = res.json()

            # fetch author name and validate other fields
            author_id = res.json()['authors'][0]['author']['key']
            author_res = requests.get(f'https://openlibrary.org{author_id}.json')
            if author_res.status_code != 200:
                return None
            author_data = author_res.json()
            author = 'unknown'
            if 'name' in author_data:
                author = author_data['name']
            elif 'personal_name' in author_data:
                author = author_data['personal_name']
            description = None
            if 'description' in book_data:
                description = book_data['description']['value'] if type(book_data['description']) == dict else book_data['description']
            subjects = []
            if 'subjects' in book_data:
                subjects = book_data['subjects']
            cover = book_data['covers'][0] if 'covers' in book_data else None

            # cache in database
            cursor.execute('INSERT INTO book_data (work_id, title, author, description, cover, subjects) VALUES (%s, %s, %s, %s, %s, %s);', (work_id, book_data['title'], author, description, cover, json.dumps(subjects)))
            cursor.close()
            db.db.commit()
            return BookData(work_id, book_data['title'], author, description, cover, subjects)
        except Exception as e:
            print(e)
            return None

class UserBook:
    def __init__(self, username, book_data: BookData, action, wtr_date=None, rng_date=None, rd_date=None):
        self.username = username
        self.book_data = book_data
        self.action = action
        self.wtr_date = wtr_date
        self.rng_date = rng_date
        self.rd_date = rd_date

    def to_dict(self):
        book_data = self.book_data.__dict__
        wtr_date = self.wtr_date.isoformat() if self.wtr_date else None
        rng_date = self.rng_date.isoformat() if self.rng_date else None
        rd_date = self.rd_date.isoformat() if self.rd_date else None
        return {'username': self.username, 'book_data': book_data, 'action': self.action, 'wtr_date': wtr_date, 'rng_date': rng_date, 'rd_date':rd_date}

    @staticmethod
    def get_books_for_user(username, work_id=None, dict=False):
        db = Database()
        cursor = db.db.cursor()
        if work_id:
            cursor.execute('SELECT work_id, action, wtr_date, rng_date, rd_date FROM user_books WHERE username = %s AND work_id = %s;', (username, work_id))
        else:
            cursor.execute('SELECT work_id, action, wtr_date, rng_date, rd_date FROM user_books WHERE username = %s;', (username,))
        books = cursor.fetchall()
        cursor.close()
        if work_id:
            if len(books) == 0:
                return None
            raw_book = books[0]
            book_data = BookData.from_work_id(raw_book[0])
            return UserBook(username, book_data, raw_book[1], raw_book[2], raw_book[3], raw_book[4])

        userbooks = []
        for book in books:
            book_data = BookData.from_work_id(book[0])
            if dict:
                userbooks.append(UserBook(username, book_data, book[1], book[2], book[3], book[4]).to_dict())
            else:
                userbooks.append(UserBook(username, book_data, book[1], book[2], book[3], book[4]))
        return userbooks

    @staticmethod
    def upsert_user_book(username, work_id, action):
        if action not in ['wtr', 'rng', 'rd']:
            raise Exception('Invalid action')
        action_int = 0
        if action == 'rng':
            action_int = 1
        elif action == 'rd':
            action_int = 2

        db= Database()
        cursor = db.db.cursor()
        cursor.execute('SELECT * FROM user_books WHERE username = %s AND work_id = %s;', (username, work_id))
        if cursor.fetchone():
            cursor.execute(f'UPDATE user_books SET action = %s, {action}_date = CURDATE() WHERE username = %s AND work_id = %s;', (action_int, username, work_id))
        else:
            cursor.execute(f'INSERT INTO user_books (username, work_id, action, {action}_date) VALUES (%s, %s, %s, CURDATE());', (username, work_id, action_int))
        cursor.close()
        db.db.commit()

def search_books(title, limit = 10):
    q = urllib.parse.urlencode({'q': title, 'limit': limit})
    res = requests.get(f'https://openlibrary.org/search.json?{q}')
    if res.status_code != 200:
        return None
    data = res.json()
    books = []
    for doc in data['docs']:
        if doc['type'] == 'work':
            work_id = doc['key'].split('/')[-1]
            title = doc['title']
            author = doc['author_name'][0] if 'author_name' in doc else 'unknown'
            cover = doc['cover_i'] if 'cover_i' in doc else None
            books.append({'work_id': work_id, 'title': title, 'author': author, 'cover': cover})
            books.sort(key=lambda x: 1 if x['cover'] else 0, reverse=True)
    return books if len(books) > 0 else None

