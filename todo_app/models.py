from pydantic import BaseModel,EmailStr, validator
from typing import List,Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def password_strength(cls, value):
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        return value

class UserLogin(BaseModel):
    email: EmailStr
    password: str

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
    status: str