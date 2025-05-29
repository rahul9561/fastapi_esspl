import sqlite3
conn= sqlite3.connect("ecom.db")
curser=conn.cursor()
import json
with open("products.json","r") as f:
        products=json.load(f)

for product in products:
    curser.execute("""
                   INSERT INTO products(title, price, description, img)
                   VALUES(?, ?, ?, ?)""",
                   (product["title"], product["price"], product["description"],
                     product["thumbnail"]))
    
conn.commit()
conn.close()
print("Products inserted successfully")
