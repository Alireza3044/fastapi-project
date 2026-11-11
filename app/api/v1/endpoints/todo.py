from typing import Annotated, Any

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.todo import TodoCreate, TodoRead
from app.services.todo import TodoService

router = APIRouter(tags=["todo"])


@router.get("", status_code=status.HTTP_200_OK, response_model=list[TodoRead])
async def get_all_todos(
    user_data: Annotated[dict[str, Any], Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = TodoService(db)
    return await service.get_all_todos(user_data["user_id"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user_data: Annotated[dict[str, Any], Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    todo_schema: TodoCreate
):
    service = TodoService(db)
    await service.create_todo(todo_schema, user_data["user_id"])
    return {"detail": "Todo created successfully"}


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=TodoRead)
async def get_todo(
    user_data: Annotated[dict[str, Any], Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    id: int = Path(ge=1)
):
    service = TodoService(db)
    return await service.get_todo(id, user_data["user_id"])


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user_data: Annotated[dict[str, Any], Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    todo_schema: TodoCreate,
    id: int = Path(ge=1)
):
    service = TodoService(db)
    await service.update_todo(id, user_data["user_id"], todo_schema)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user_data: Annotated[dict[str, Any], Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    id: int = Path(ge=1)
):
    service = TodoService(db)
    await service.delete_todo(id, user_data["user_id"])
