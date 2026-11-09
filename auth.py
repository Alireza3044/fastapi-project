from jose import jwt, JWTError
from decouple import config
from datetime import timedelta, datetime, timezone
from typing import Annotated, TypeAlias
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from starlette import status

from database import DB_DEP
from models import User
from utils import check_password

oauth2_bearer = OAuth2PasswordBearer("/auth/token")

ALGORITHM = config("JWT_ALGORITHM")
SECRET_KEY = config("SECRET_KEY")


def authenticate_user(username: str, password: str, db: DB_DEP) -> User | None:
    user = db.query(User).filter_by(username=username).first()
    
    if not user:
        return
    if not check_password(str(user.hashed_password), password):
        return
    return user


def generate_access_token(user_id: int, username: str, expires_delta: timedelta):
    expires = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": username, "user_id": user_id, "exp": expires}
    return jwt.encode(payload, SECRET_KEY, ALGORITHM) # type: ignore


def get_current_user_id(token: Annotated[str, Depends(oauth2_bearer)], db: DB_DEP) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM) # type: ignore
        username = payload.get("username")
        user_id = payload.get("user_id")

        if username is None or user_id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Could not validate user.")        
        return user_id

    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Could not validate user.")


USER_ID_DEP: TypeAlias = Annotated[int, Depends(get_current_user_id)]
