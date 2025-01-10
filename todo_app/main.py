from fastapi import FastAPI, HTTPException
from datetime import datetime
from . models import ToDoCreate, ToDo
from . db import setup_database, get_db
from typing import List

app = FastAPI(title="ToDo API")

setup_database()

@app.post("/todos/", response_model=ToDo)
async def create_todo(todo: ToDoCreate):
    try:
        conn = get_db()
        cursor = conn.cursor()
        created_at = datetime.now().isoformat()
        cursor.execute('INSERT INTO todos (title, description, due_date, created_at) VALUES (?, ?, ?, ?)', 
                       (todo.title, todo.description, todo.due_date, created_at))
        todo_id = cursor.lastrowid
        conn.commit()
        cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
        todo_data = cursor.fetchone()
        if todo_data is None:
            raise HTTPException(status_code=404, detail="Failed to create todo")
        return dict(todo_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/todos/", response_model=List[ToDo])
async def get_todos():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM todos')
        todos = [dict(row) for row in cursor.fetchall()]
        return todos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching todos: {str(e)}")

@app.get("/todos/{todo_id}", response_model=ToDo)
async def get_todo(todo_id: int):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
        todo = cursor.fetchone()
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return dict(todo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching todo: {str(e)}")
