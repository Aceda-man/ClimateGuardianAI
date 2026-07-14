import sqlite3

connection = sqlite3.connect('climate_guardian.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    password TEXT,
    state TEXT,
    lga TEXT,
    community TEXT,
    user_type TEXT
)
""")