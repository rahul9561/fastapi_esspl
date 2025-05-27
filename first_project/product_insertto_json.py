import sqlite3
import json

# Connect to the database (or create it)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()


# Load data from JSON file
with open("product.json", "r") as file:
    products = json.load(file)

# Insert data into the table
for product in products['products']:
    cursor.execute("""
    INSERT INTO product (name, description, category, price,  stock, image)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        product.get("title"),
        product.get("description"),
        product.get("category"),
        product.get("price"),
        product.get("stock"),
        product.get("thumbnail")
    ))

# Commit and close
conn.commit()
conn.close()

print("✅ Products inserted successfully into database.db")
