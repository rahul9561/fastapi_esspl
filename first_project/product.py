import sqlite3
conn=sqlite3.connect("database.db")
cursor=conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        image TEXT,
        category TEXT NOT NULL
               
    )
""")

conn.commit()
conn.close()