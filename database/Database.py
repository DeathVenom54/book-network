import mysql.connector as connector

class Database:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.db = None

    def connect(self):
        self.db = connector.connect(host=self.host, user=self.user, password=self.password)
        cursor = self.db.cursor()
        with open('database/definition.sql', 'r') as file:
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

    class Book:
        def __init__(self, user, title, author, genre, description, cover_url, book_url):
            self.user = user
            self.title = title
            self.author = author
            self.genre = genre
            self.description = description
            self.cover_url = cover_url
            self.book_url = book_url


class UserExistsException(Exception): ...

# testing
if __name__ == '__main__':
    db = Database('localhost', 'root', 'passmysql')
    db.connect()
    db.create_user('dv', 'dv', 'DV Display Name', 'I am the creator of this website', '100')
    print('Test passed')