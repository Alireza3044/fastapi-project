from fastapi import APIRouter, Path
from fastapi.exceptions import HTTPException
from starlette import status

from database import DB_DEP
from auth import USER_DEP
from models import Todo

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/todo", status_code=status.HTTP_200_OK)
def get_all_todos(user: USER_DEP, db: DB_DEP):
    if user["role"].lower() != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only admins can access this endpoint.")
    return db.query(Todo).all()


@router.get("/todo/{id}", status_code=status.HTTP_200_OK)
def get_todo(user: USER_DEP, db: DB_DEP, id: int = Path(ge=1)):
    if user["role"].lower() != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only admins can access this endpoint.")
    
    todo = db.get(Todo, id)
    
    if not todo:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "todo not found.")
    return todo


@router.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user: USER_DEP, db: DB_DEP, id: int = Path(ge=1)):
    if user["role"].lower() != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only admins can access this endpoint.")
    
    todo = db.get(Todo, id)
    
    if not todo:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "todo not found.")

    db.delete(todo)
    db.commit()
