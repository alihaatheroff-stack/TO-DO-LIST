from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import todo

app = FastAPI(
    title="Todo App",
    description="A professional Todo API with CI/CD pipeline",
    version="1.0.0"
)

ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')


class CreateTodoRequest(BaseModel):
    title: str
    description: Optional[str] = ""


class UpdateTodoRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


@app.get("/")
def home():
    return {
        "message": "Todo App is running!",
        "environment": ENVIRONMENT,
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "environment": ENVIRONMENT
    }


@app.post("/todos", status_code=201)
def create_todo(request: CreateTodoRequest):
    try:
        new_todo = todo.create_todo(
            title=request.title,
            description=request.description
        )
        return new_todo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/todos")
def get_all_todos():
    all_todos = todo.get_all_todos()
    return {
        "count": len(all_todos),
        "todos": all_todos
    }


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    try:
        return todo.get_todo_by_id(todo_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, request: UpdateTodoRequest):
    try:
        updated = todo.update_todo(
            todo_id=todo_id,
            title=request.title,
            description=request.description,
            completed=request.completed
        )
        return updated
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    try:
        deleted = todo.delete_todo(todo_id)
        return {
            "message": "Todo deleted successfully",
            "deleted_todo": deleted
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))