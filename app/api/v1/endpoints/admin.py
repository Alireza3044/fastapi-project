from typing import Annotated, Any

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.todo import TodoRead
from app.services.admin import AdminService

router = APIRouter(tags=["admin"])


@router.get(
    "/todo", status_code=status.HTTP_200_OK, response_model=list[TodoRead]
)
async def get_all_todos(
    user_data: Annotated[dict[str, Any], Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = AdminService(db, user_data["role"])
    return await service.get_all_todos()


@router.get(
    "/todo/{id}", status_code=status.HTTP_200_OK, response_model=TodoRead
)
async def get_todo(
    user_data: Annotated[dict[str, Any], Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    id: int = Path(ge=1)
):
    service = AdminService(db, user_data["role"])
    return await service.get_todo(id)


@router.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user_data: Annotated[dict[str, Any], Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    id: int = Path(ge=1)
):
    service = AdminService(db, user_data["role"])
    await service.delete_todo(id)
