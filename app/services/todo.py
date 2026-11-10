from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.todo import Todo
from app.schemas.todo import TodoCreate


class TodoService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_todos(self, owner_id: int):
        result = await self.db.execute(
            select(Todo).where(Todo.owner_id == owner_id)
        )
        return list(result.scalars().all())

    async def create_todo(self, todo_schema: TodoCreate, owner_id: int):
        todo = Todo(**todo_schema.model_dump(), owner_id=owner_id)
        self.db.add(todo)

        await self.db.flush()
        await self.db.refresh(todo)
        return todo

    async def get_todo(self, id: int, owner_id: int) -> Todo:
        result = await self.db.execute(
            select(Todo).where(Todo.id == id, Todo.owner_id == owner_id)
        )
        todo = result.scalar_one_or_none()

        if todo is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Todo not found")
        return todo

    async def update_todo(
        self, id: int, owner_id: int, todo_schema: TodoCreate
    ) -> Todo:
        todo = await self.get_todo(id, owner_id)

        for field, value in todo_schema.model_dump(exclude_unset=True).items():
            setattr(todo, field, value)

        await self.db.flush()
        await self.db.refresh(todo)
        return todo

    async def delete_todo(self, id: int, owner_id: int):
        todo = await self.get_todo(id, owner_id)
        await self.db.delete(todo)
