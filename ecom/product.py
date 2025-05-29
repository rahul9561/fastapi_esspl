import sqlite3
conn=sqlite3.connect("ecom.db")
curser=conn.cursor()

curser.execute("""
               
               CREATE TABLE products(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT NOT NULL,
               price REAL NOT NULL,
               description TEXT NOT NULL,
               img TEXT NOT NULL

               )
               
               """)

conn.commit()
conn.close()