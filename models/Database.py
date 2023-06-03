import mysql.connector as connector
from models.Book import BookData


class Database:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.db = None

    def connect(self):
        self.db = connector.connect(host=self.host, user=self.user, password=self.password)
        cursor = self.db.cursor()
        with open('models/definition.sql', 'r') as file:
            for line in file:
                cursor.execute(line)
        cursor.close()
        self.db.commit()

    def create_user(self, username, password, display_name = None, bio = None):
        # check if user already exists
        cursor = self.db.cursor()
        cursor.execute('SELECT username FROM users WHERE username = %s;', (username,))
        user = cursor.fetchone()
        if user:
            raise UserExistsException()

        cursor.execute('INSERT INTO users (username, password, display_name, bio) VALUES (%s, %s, %s, %s);', (username, password, display_name, bio))
        cursor.close()
        self.db.commit()
        return User(username, self.db, display_name, bio)

    def get_user (self, username):
        cursor = self.db.cursor()
        cursor.execute('SELECT password, display_name, bio FROM users WHERE username = %s;', (username,))
        user = cursor.fetchone()
        if user:
            return User(username, user[0], self.db, display_name=user[1], bio=user[2])
        else:
            return None

class UserBook:
    def __init__(self, username, book_data, action, wtr_date=None, rng_date=None, rd_date=None):
        self.username = username
        self.book_data = book_data
        self.action = action
        self.wtr_date = wtr_date
        self.rng_date = rng_date
        self.rd_date = rd_date


class User:
    def __init__(self, username, password, db, display_name = None, bio = None):
        self.username = username
        self.password = password
        self.display_name = display_name
        self.bio = bio
        self.db = db

    def get_safe_user(self):
        return User(self.username, '', self.db, self.display_name, self.bio)

    def update(self, display_name = None, bio = None):
        cursor = self.db.cursor()
        dn = display_name if display_name else self.display_name
        b = bio if bio else self.bio
        cursor.execute('UPDATE users SET display_name = %s, bio = %s WHERE username = %s;', (dn, b, self.username))
        cursor.close()
        self.db.commit()
        self.display_name = dn
        self.bio = b

    def get_books(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT work_id, action, wtr_date, rng_date, rd_date FROM user_books WHERE username = %s;', (self.username,))
        books = cursor.fetchall()
        print(books)
        cursor.close()
        userbooks = []
        for book in books:
            book_data = BookData.from_work_id(book[0])
            userbooks.append(UserBook(self.username, book_data, book[1], book[2], book[3], book[4]))
        return userbooks

class UserExistsException(Exception): ...
