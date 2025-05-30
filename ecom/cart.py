# cart.py
import sqlite3
conn = sqlite3.connect("ecom.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS carts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
)

""")

conn.commit()
conn.close()