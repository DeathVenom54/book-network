import json
import urllib.parse

import requests

import models.db
from models.db import get_db


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
            db = get_db()
            cursor = db.cursor()
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
            models.db.db.commit()
            return BookData(work_id, book_data['title'], author, description, cover, subjects)
        except Exception as e:
            print(e)
            return None


def search_books(title):
    q = urllib.parse.urlencode({'title': title, 'fields': 'key,type'})
    res = requests.get(f'https://openlibrary.org/search.json?{q}')
    if res.status_code != 200:
        return None
    data = res.json()
    ids = []
    for doc in data['docs']:
        if doc['type'] == 'work':
            ids.append(doc['key'].split('/')[-1])
    return ids if len(ids) > 0 else None