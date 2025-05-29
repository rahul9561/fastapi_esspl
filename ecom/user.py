import sqlite3
conn= sqlite3.connect("ecom.db")
cursor= conn.cursor()
cursor.execute("""
               CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL UNIQUE,
               password TEXT NOT NULL,
               email TEXT NOT NULL UNIQUE
               )
               """)

conn.commit()
conn.close()