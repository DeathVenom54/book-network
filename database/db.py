from database.Database import Database

db = Database('localhost', 'root', 'passmysql')

def connect_to_db():
    db.connect()

def get_db():
    return db