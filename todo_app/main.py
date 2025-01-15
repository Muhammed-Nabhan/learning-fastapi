from fastapi import FastAPI,HTTPException
from datetime import datetime
from . models import ToDoCreate, ToDo,UserCreate, UserLogin
from . db import setup_database, get_db
from typing import List
from todo_app.routes.todos import router as todos_router
from .auth import register_user, authenticate_user
from .exceptions import raise_401

app = FastAPI(title="ToDo API")



setup_database()

logged_in_users = {}

@app.post("/register/")
async def register(user: UserCreate):
    return register_user(user.email, user.password)

@app.post("/login/")
async def login(user: UserLogin):
    user_data = authenticate_user(user.email, user.password)
    # Create a session
    logged_in_users[user_data["id"]] = user_data
    return {"message": "Login successful", "user_id": user_data["id"]}


app.include_router(todos_router, prefix="/api", tags=["ToDos"])

@app.post("/todos/", response_model=ToDo)
async def create_todo(todo: ToDoCreate,user_id: int):
    if user_id not in logged_in_users:
        raise_401("User not logged in.")
    try:
        conn = get_db()
        cursor = conn.cursor()
        created_at = datetime.now().isoformat()
        cursor.execute('INSERT INTO todos (title, description, due_date, created_at,user_id) VALUES (?, ?, ?, ?,?)', 
                       (todo.title, todo.description, todo.due_date, created_at,user_id))
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
async def get_todos(user_id: int):
    if user_id not in logged_in_users:
        raise_401("User not logged in.")
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM todos WHERE user_id = ?',(user_id,))
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
