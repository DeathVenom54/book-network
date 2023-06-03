from models.Database import Database

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'passmysql'

db = Database(DB_HOST, DB_USER, DB_PASSWORD)


def connect_to_db():
    db.connect()
    print('Connected to database')


def get_db():
    return db
