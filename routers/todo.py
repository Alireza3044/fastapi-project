from fastapi import APIRouter, Path
from fastapi.exceptions import HTTPException
from starlette import status

from database import DB
from models import Todo
from serializers import TodoSerializer

router = APIRouter(tags=["todo"])


@router.get("/todo", status_code=status.HTTP_200_OK)
def get_all_todos(db: DB):
    return db.query(Todo).all()


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: DB, tr: TodoSerializer):
    todo = Todo(**tr.model_dump())
    db.add(todo)
    db.commit()


@router.get("/todo/{id}", status_code=status.HTTP_200_OK)
def get_todo(db: DB, id: int = Path(ge=1)):
    todo = db.get(Todo, id)
    
    if not todo:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "todo not found.")
    return todo


@router.put("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(db: DB, tr: TodoSerializer, id: int = Path(ge=1)):
    todo = db.get(Todo, id)
    
    if not todo:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "todo not found.")

    for field, value in tr.model_dump().items():
        setattr(todo, field, value)
    db.commit()


@router.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db: DB, id: int = Path(ge=1)):
    todo = db.get(Todo, id)
    
    if not todo:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "todo not found.")

    db.delete(todo)
    db.commit()
