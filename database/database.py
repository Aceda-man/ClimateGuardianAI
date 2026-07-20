import sqlite3
from pathlib import Path

# ==========================================
# DATABASE LOCATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "climate.db"


# ==========================================
# CONNECTION
# ==========================================

def get_connection():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    # Enable Foreign Keys
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


# ==========================================
# CREATE DATABASE
# ==========================================

def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    # ======================================
    # USERS
    # ======================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        full_name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        username TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        state TEXT NOT NULL,

        lga TEXT NOT NULL,

        community TEXT NOT NULL,

        user_type TEXT NOT NULL,

        security_question TEXT NOT NULL,

        security_answer TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ======================================
    # INCIDENT REPORTS
    # ======================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        incident_type TEXT NOT NULL,

        severity TEXT NOT NULL,

        title TEXT NOT NULL,

        description TEXT NOT NULL,

        image_path TEXT,

        state TEXT NOT NULL,

        lga TEXT NOT NULL,

        community TEXT NOT NULL,

        status TEXT DEFAULT 'Pending',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # ======================================
    # REPORT VERIFICATIONS
    # ======================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS report_verifications (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        report_id INTEGER NOT NULL,

        user_id INTEGER NOT NULL,

        vote TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        UNIQUE(report_id, user_id),

        FOREIGN KEY(report_id) REFERENCES reports(id),

        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # ======================================
    # COMMUNITY POSTS
    # ======================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS community_posts (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        content TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # ======================================
    # COMMENTS
    # ======================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        report_id INTEGER NOT NULL,

        user_id INTEGER NOT NULL,

        comment TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(report_id) REFERENCES reports(id),

        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


# ==========================================
# RUN FILE DIRECTLY
# ==========================================

if __name__ == "__main__":
    create_database()