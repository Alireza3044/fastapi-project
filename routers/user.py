from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from starlette import status
from typing import Annotated
from datetime import timedelta

from serializers import UserSerializer, TokenSerializer
from utils import hash_password
from models import User
from database import DB_DEP
from auth import authenticate_user, generate_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(db: DB_DEP, u: UserSerializer):
    raw_user = u.model_dump()

    # Remove raw password and set hashed password
    raw_pass = raw_user.pop("password")
    hashed = hash_password(raw_pass)
    user = User(**raw_user, hashed_password=hashed)

    db.add(user)
    db.commit()


@router.post("/token", status_code=status.HTTP_200_OK, response_model=TokenSerializer)
async def get_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DB_DEP):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid credentials.")

    token = generate_access_token(user.id, user.username, timedelta(minutes=20)) # type: ignore
    return {"access_token": token, "token_type": "bearer"}
