from jose import jwt
from datetime import timedelta, datetime, timezone
from typing import Annotated, TypeAlias, Any
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import get_settings
from app.db.session import DB_DEP
from app.core.dependencies import get_current_user
from app.db.models.user import User
from app.utils import check_password

settings = get_settings()

oauth2_bearer = OAuth2PasswordBearer("/auth/token")


def authenticate_user(username: str, password: str, db: DB_DEP) -> User | None:
    user = db.query(User).filter_by(username=username).first()
    
    if not user:
        return
    if not check_password(str(user.hashed_password), password):
        return
    return user


def generate_access_token(user_id: int, username: str, role: str, expires_delta: timedelta):
    expires = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": username, "user_id": user_id, "role": role, "exp": expires}
    return jwt.encode(payload, settings.SECRET_KEY, settings.JWT_ALGORITHM)


USER_DEP: TypeAlias = Annotated[dict[str, Any], Depends(get_current_user)]
