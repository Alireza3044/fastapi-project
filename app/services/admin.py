from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.todo import Todo


class AdminService:
    def __init__(self, db: AsyncSession, role: str):
        self.db = db

        # If not admin, no service is allowed
        if not role.lower() == "admin":
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Only admins can access this endpoint"
            )

    async def get_all_todos(self):
        result = await self.db.execute(
            select(Todo)
        )
        return list(result.scalars().all())

    async def get_todo(self, id: int) -> Todo:
        result = await self.db.execute(
            select(Todo).where(Todo.id == id)
        )
        todo = result.scalar_one_or_none()

        if todo is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Todo not found")
        return todo

    async def delete_todo(self, id: int):
        todo = await self.get_todo(id)
        await self.db.delete(todo)
