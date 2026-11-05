from fastapi import APIRouter, HTTPException

from app import storage
from app.utils import now_iso

router = APIRouter()


@router.post("/todos")
def create_todo(title: str):
    if not title.strip():
        raise HTTPException(status_code=422, detail="title required")
    todo = storage.add_todo(title.strip(), created_at=now_iso())
    return todo.to_dict()


@router.get("/todos")
def list_todos():
    return [t.to_dict() for t in storage.all_todos()]
