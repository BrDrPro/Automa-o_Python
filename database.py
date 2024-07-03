import sqlite3

db = sqlite3.connect('database.sqlite')

cursor = db.cursor()

def create_table():
    cursor.execute('''
        CREATE TABLE ativos(
            id INTEGER PRIMARY KEY, details JSON)
    ''')
    db.commit()
create_table()