# Expense Tracker

A desktop expense tracker built with Python and CustomTkinter (CTk).

This is my first GUI application, created to learn how Python can be used to build a complete desktop application with a graphical interface, user accounts, and a local SQL database.

## Features

- 🖥️ Desktop GUI application built with CustomTkinter
- 👥 Multiple-user account system
- 🔐 Passwords are stored in hashed form
- 💾 Expense data is stored locally on the user's computer
- 🗄️ Uses an SQL database for storing accounts and expenses
- 📊 Track and manage personal expenses
- 🗑️ Add, view, and delete expenses
- 👤 Separate data for each user
- 📦 Available as both Python source code and an `.exe` release

## Built With

- **Python**
- **CustomTkinter** — GUI
- **SQLite** — Local SQL database
- **datetime** — Date handling

## How It Works

The application uses a local SQLite database stored on the user's computer.

Each user has their own account and expenses are associated with their user ID, so different users can use the same application without sharing their expense records.

Passwords are not stored as plain text. They are stored in hashed form in the database.

## How to Run Programm

### Requirements

- Python 3.x
- CustomTkinter

Install the required external package:

```bash
pip install -r requirements.txt
```

### Run

Make sure Python 3.x is installed on your computer with required packages.

Clone this repository:

```bash
git clone https://github.com/anshulsxd/gui-multiuser-expense-tracker.git
```

Run the application:
```bash
py main.py
```
or 
```bash
python main.py
```