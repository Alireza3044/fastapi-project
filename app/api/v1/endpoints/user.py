from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from typing import Annotated
from datetime import timedelta

from serializers import UserSerializer, TokenSerializer, ChangePasswordSerializer
from utils import hash_password, check_password
from models import User
from database import DB_DEP
from auth import authenticate_user, generate_access_token, USER_DEP

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(db: DB_DEP, u: UserSerializer):
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

    token = generate_access_token(user.id, user.username, user.role, timedelta(minutes=20)) # type: ignore
    return {"access_token": token, "token_type": "bearer"}


@router.get("/profile", status_code=status.HTTP_200_OK)
async def profile(user: USER_DEP, db: DB_DEP):
    return db.get(User, user["user_id"])


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(input_data: ChangePasswordSerializer, u: USER_DEP, db: DB_DEP):
    user = db.get(User, u["user_id"])
    data = input_data.model_dump()

    if not check_password(user.hashed_password, data.get("old_password")): # type: ignore
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "old_password is not valid.")

    if data.get("old_password") == data.get("new_password"):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "new password must not be the same as old password.")

    user.hashed_password = hash_password(input_data.new_password) # type: ignore
    db.commit()
