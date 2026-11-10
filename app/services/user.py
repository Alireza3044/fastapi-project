from typing import Optional

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.schemas.user import PasswordChange, UserCreate
from app.utils import check_password, hash_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, data: UserCreate) -> User:
        raw_user = data.model_dump()

        # Remove raw password and set hashed password
        raw_pass = raw_user.pop("password")
        hashed = hash_password(raw_pass)
        user = User(**raw_user, hashed_password=hashed)

        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def get_user(
        self,
        *,
        id: Optional[int] = None,
        username: Optional[str] = None
    ) -> User:
        result: Result[User]
        if id:
            result = await self.db.execute(
                select(User).where(User.id == id)
            )
        elif username:
            result = await self.db.execute(
                select(User).where(User.username == username)
            )
        else:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Id or username is required to get user"
            )

        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        return user

    async def change_password(
        self,
        user_id: int,
        pass_data: PasswordChange
    ) -> User:
        user = await self.get_user(id=user_id)
        data = pass_data.model_dump()

        is_valid = check_password(
            user.hashed_password,  # type: ignore
            data.get("old_password")  # type: ignore
        )
        if not is_valid:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_CONTENT,
                "old_password is not valid."
            )

        if data.get("old_password") == data.get("new_password"):
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_CONTENT,
                "new password must not be the same as old password."
            )

        user.hashed_password = hash_password(  # type: ignore
            data.new_password  # type: ignore
        )
        await self.db.flush()
        await self.db.refresh(user)
        return user
