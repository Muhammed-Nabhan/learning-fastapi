import sqlite3
from fastapi import HTTPException

def setup_database():
    try:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT, due_date TEXT, created_at TEXT NOT NULL)''')
        conn.commit()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error setting up database")

def get_db():
    try:
        conn = sqlite3.connect('todo.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection error")
