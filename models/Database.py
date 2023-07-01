import mysql.connector as connector
from routers.api.auth import hash_password
# Singleton pattern, only one instance of Database
# can exist and can be called from anywhere
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=Singleton):
    host = None
    user = None
    password = None

    def __init__(self, host='', user='', password=''):
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

class User:
    def __init__(self, username, password, db, display_name = None, bio = None):
        self.username = username
        self.password = password
        self.display_name = display_name
        self.bio = bio
        self.db = db

    def get_safe_user(self):
        return User(self.username, '', self.db, self.display_name, self.bio)

    def get_friends(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT user1, user2 FROM friends WHERE user1 = ? OR user2 = ?', (self.username, self.username))
        rows = cursor.fetchall()
        cursor.close()
        friends = []
        for row in rows:
            username = row[0] if row[1] == self.username else row[1]
            friends.append(self.db.get_user(username))
        return friends

    def get_friend_reqs(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT u_from, u_to FROM friend_requests WHERE u_from = ? OR u_to = ?', (self.username, self.username))
        rows = cursor.fetchall()
        sent = []
        received = []
        for row in rows:
            if row[0] == self.username:
                user = self.db.get_user(row[1])
                sent.append(user)
            else:
                user = self.db.get_user(row[1])
                received.append(user)
        cursor.close()
        return {'sent': sent, 'received': received}

    def accept_friend_req(self, other):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM friend_requests WHERE u_to = ?', (self.username,))
        if not cursor.fetchone:
            raise Exception('No request found')
        cursor.execute('INSERT INTO friends VALUES (?, ?)', (self.username, other))
        cursor.execute('DELETE FROM friend_requests WHERE u_to = ? AND u_from = ?', (self.username, other))
        cursor.close()
        self.db.commit()

    def send_friend_req(self, other):
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO friend_requests (u_from, u_to) VALUES (?, ?)', (self.username, other))
        cursor.close()
        self.db.commit()


    def update(self, username=None, password=None, display_name = None, bio = None):
        cursor = self.db.cursor()
        dn = display_name if display_name else self.display_name
        b = bio if bio else self.bio
        un = username if username else self.username
        p = password if password else self.password
        if p == '':
            raise Exception('Cannot update user without password')
        cursor.execute('UPDATE users SET username = %s, password = %s, display_name = %s, bio = %s WHERE username = %s;', (un, hash_password(p), dn, b, self.username))
        cursor.close()
        self.db.commit()
        self.username = un
        self.password = p
        self.display_name = dn
        self.bio = b

class UserExistsException(Exception): ...
