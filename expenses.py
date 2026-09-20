import sqlite3
import os
from datetime import date
from datetime import datetime

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
            title TEXT NOT NULL,
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


def add_expense(user_id, title, amount, category, description):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    today = date.today().isoformat()

    cursor.execute("""
        INSERT INTO expenses
        (user_id, title, amount, category, description, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        title,
        amount,
        category,
        description,
        today
    ))

    conn.commit()
    conn.close()


def get_expenses(user_id, date_value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, amount, category, description, date
        FROM expenses
        WHERE user_id = ? AND date = ?
        ORDER BY id DESC
    """, (user_id, date_value,))

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

def get_total_exp(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(amount) FROM expenses WHERE user_id = ?""", (user_id,)
    )

    total = cursor.fetchone()[0]
    conn.close()

    if total is None:
        return 0

    return total

def get_this_month(user_id):
    this_month = datetime.now().strftime("%Y-%m")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE user_id = ? AND strftime('%Y-%m', date) = ?""",
        (user_id, this_month)
        )

    this_month_total = cursor.fetchone()[0]

    conn.close()

    return this_month_total

def get_total_entries(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM expenses WHERE user_id = ?""", (user_id,)
        )

    total_entries = cursor.fetchone()[0]

    conn.close()
    return total_entries