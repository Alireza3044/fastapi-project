from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.models.user import User
from app.db.session import get_db
from app.services.user import UserService
from app.utils import check_password

settings = get_settings()


async def authenticate_user(
    username: str,
    password: str,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    service = UserService(db)
    user = await service.get_user(username=username)

    if not check_password(str(user.hashed_password), password):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            "Invalid username or password"
        )
    return user


def generate_access_token(
    user_id: int,
    username: str,
    role: str,
    expires_delta: timedelta
) -> str:
    expires = datetime.now(timezone.utc) + expires_delta
    payload = {
        "sub": username,
        "user_id": user_id,
        "role": role,
        "exp": expires
    }
    return jwt.encode(payload, settings.SECRET_KEY, settings.JWT_ALGORITHM)
