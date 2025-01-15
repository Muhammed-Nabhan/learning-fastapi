import sqlite3
from .exceptions import raise_500

def setup_database():
    try:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT, due_date TEXT, created_at TEXT NOT NULL,status TEXT DEFAULT 'not done'
                       )''')
        conn.commit()
        
        
        cursor.execute("PRAGMA table_info(todos)")
        columns = [column[1] for column in cursor.fetchall()]
        if "status" not in columns:
            # Add the "status" column if it doesn't exist
            cursor.execute("ALTER TABLE todos ADD COLUMN status TEXT DEFAULT 'not done'")
            conn.commit()
        if "user_id" not in columns:
            cursor.execute("ALTER TABLE todos ADD COLUMN user_id INTEGER DEFAULT -1 NOT NULL")
            conn.commit()
        conn.close()
    except Exception as e:
        raise_500("Error setting up database")

def get_db():
    try:
        conn = sqlite3.connect('todo.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
         raise_500("Database connection error")
