import sqlite3
from fastapi import HTTPException
from .db import get_db
from .exceptions import raise_400,raise_401

def register_user(email: str, password: str):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
        conn.commit()
        user_id = cursor.lastrowid
        return {"user_id": user_id, "email": email}
    except sqlite3.IntegrityError:
        raise_400("Email is already registered.")
    finally:
        conn.close()

def authenticate_user(email: str, password: str):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()
        if user is None:
             raise_401("Invalid credentials.")
        return dict(user)
    finally:
        conn.close()
