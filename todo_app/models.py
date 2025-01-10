from pydantic import BaseModel
from typing import List

class ToDoCreate(BaseModel):
    title: str
    description: str
    due_date: str

class ToDo(BaseModel):
    id: int
    title: str
    description: str
    due_date: str
    created_at: str
