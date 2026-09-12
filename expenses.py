import sqlite3
import os

app_dir = os.path.join(os.getenv("APPDATA"), "ExpenseTracker")
os.makedirs(app_dir, exist_ok=True)
DB_NAME = os.path.join(app_dir, "expensesDataBase.db")

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,

            FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def add_expense(user_id, amount, category, description, date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (user_id, amount, category, description, date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        amount,
        category,
        description,
        date
    ))

    conn.commit()
    conn.close()


def get_expenses(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, amount, category, description, date
        FROM expenses
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    expenses = cursor.fetchall()

    conn.close()

    return expenses


def delete_expense(expense_id, user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ? AND user_id = ?
    """, (expense_id, user_id))

    conn.commit()
    conn.close()