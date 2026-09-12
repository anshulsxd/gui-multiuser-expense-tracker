import sqlite3
import hashlib
import os

app_dir = os.path.join(os.getenv("APPDATA"), "ExpenseTracker")
os.makedirs(app_dir, exist_ok=True)
DB_NAME = os.path.join(app_dir, "expensesDataBase.db")


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def create_account(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, (username, hashed_password))

        conn.commit()
        conn.close()

        return True

    except sqlite3.IntegrityError:
        return False


def login(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM users
        WHERE username = ? AND password = ?
    """, (username, hashed_password))

    user = cursor.fetchone()

    conn.close()

    if user:
        return user[0]
    else:
        return None