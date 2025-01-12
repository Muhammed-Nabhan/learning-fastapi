from fastapi import APIRouter, HTTPException
from todo_app.db import get_db
from todo_app.models import ToDo
from todo_app.exceptions import raise_404, raise_500

router = APIRouter()

@router.patch("/todos/{todo_id}/status", response_model=ToDo)
async def update_todo_status(todo_id: int, status: str):
    if status not in ['done', 'not done']:
        raise HTTPException(status_code=400, detail="Invalid status. Use 'done' or 'not done'.")

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE todos SET status = ? WHERE id = ?", (status, todo_id))
        if cursor.rowcount == 0:
            raise_404("ToDo item not found")
        conn.commit()
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        todo = cursor.fetchone()
        if todo is None:
            raise_404("ToDo item not found")
        return dict(todo)
    except Exception as e:
        raise_500(f"Error updating ToDo status: {str(e)}")

@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        if cursor.rowcount == 0:
            raise_404("ToDo item not found")
        conn.commit()
        return {"message": f"ToDo item with id {todo_id} deleted successfully"}
    except Exception as e:
        raise_500(f"Error deleting ToDo: {str(e)}")
