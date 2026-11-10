from jose import jwt, JWTError
from typing import Annotated, Any
from fastapi import Depends, status
from fastapi.exceptions import HTTPException

from app.db.session import DB_DEP
from app.core.security import oauth2_bearer


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db: DB_DEP) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM) # type: ignore
        user_id = payload.get("user_id")
        username = payload.get("sub")
        role = payload.get("role")

        if username is None or user_id is None or role is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Could not validate user.")        
        
        return {
            "user_id": user_id,
            "username": username,
            "role": role
        }

    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Could not validate user.")