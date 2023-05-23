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
        cursor.execute("CREATE DATABASE IF NOT EXISTS book_network;")
        cursor.execute("USE book_network;")
        cursor.execute('CREATE TABLE IF NOT EXISTS users (username VARCHAR(30) PRIMARY KEY, password VARCHAR(255) NOT NULL, display_name VARCHAR(30), bio VARCHAR(500), last_ip VARCHAR(30));')
        cursor.close()
        self.db.commit()

    def create_user(self, username, password, display_name = None, bio = None, last_ip = None):
        # check if user already exists
        cursor = self.db.cursor()
        cursor.execute('SELECT username FROM users WHERE username = %s;', (username,))
        user = cursor.fetchone()
        if user:
            raise UserExistsException()

        cursor.execute('INSERT INTO users (username, password, display_name, bio, last_ip) VALUES (%s, %s, %s, %s, %s);', (username, password, display_name, bio, last_ip))
        cursor.close()
        self.db.commit()
        return User(username, self.db, display_name, bio)

    def authenticate (self, username, password, last_ip):
        cursor = self.db.cursor()
        cursor.execute('SELECT (display_name, bio, last_ip) FROM users WHERE username = %s AND password = %s;', (username, password))
        user = cursor.fetchone()
        if last_ip != user[2]:
            cursor.execute('UPDATE users SET last_ip = %s WHERE username = %s;', (last_ip, username))
        cursor.close()
        if user:
            return User(username, self.db, display_name=user[0], bio=user[1])
        else:
            return None


class User:
    def __init__(self, username, db, display_name = None, bio = None):
        self.username = username
        self.display_name = display_name
        self.bio = bio
        self.db = db

    def update(self, display_name = None, bio = None, last_ip = None):
        cursor = self.db.cursor()
        dn = display_name if display_name else self.display_name
        b = bio if bio else self.bio
        li = last_ip if last_ip else self.last_ip
        cursor.execute('UPDATE users SET display_name = %s, bio = %s, last_ip = %s WHERE username = %s;', (dn, b, li, self.username))
        cursor.close()
        self.db.commit()


class UserExistsException(Exception): ...

# testing
if __name__ == '__main__':
    db = Database('localhost', 'root', 'passmysql')
    db.connect()
    db.create_user('dv', 'dv', 'DV Display Name', 'I am the creator of this website', '100')
    print('Test passed')