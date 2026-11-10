from typing import Any

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import get_settings

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer("/api/v1/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict[str, Any]:
    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Could not validate credentials",
        {"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.JWT_ALGORITHM
        )
        user_id: str | None = payload.get("user_id")
        username: str | None = payload.get("sub")
        role: str | None = payload.get("role")

        if user_id is None or username is None or role is None:
            raise credentials_exception

        return {
            "user_id": user_id,
            "username": username,
            "role": role
        }

    except JWTError:
        raise credentials_exception
