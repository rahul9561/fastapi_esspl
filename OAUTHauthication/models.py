import sqlite3 as sql
conn=sql.connect('OAUTHauthentication.db')
c=conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)''')
conn.commit()
conn.close()
