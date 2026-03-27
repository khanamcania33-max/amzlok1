import sqlite3

conn = sqlite3.connect("products.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    score REAL,
    analysis TEXT
)
""")

def save_product(name, score, analysis):
    cursor.execute(
        "INSERT INTO products (name, score, analysis) VALUES (?, ?, ?)",
        (name, score, analysis)
    )
    conn.commit()

def get_saved():
    cursor.execute("SELECT name, score FROM products ORDER BY score DESC")
    return cursor.fetchall()
