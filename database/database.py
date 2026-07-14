import sqlite3


DATABASE = "database/climate.db"


def create_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        state TEXT,
        lga TEXT,
        user_type TEXT
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        location TEXT,
        report_type TEXT,
        description TEXT,
        date TEXT
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS climate_data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT,
        temperature REAL,
        rainfall TEXT,
        risk_level TEXT
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agriculture(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category TEXT,
        problem TEXT
    )
    """)


    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()