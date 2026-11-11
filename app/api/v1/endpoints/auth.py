from typing import Annotated, Any

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.token import TokenRead
from app.schemas.user import PasswordChange, UserCreate, UserRead
from app.services.token import TokenService
from app.services.user import UserService

router = APIRouter(tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: UserCreate
):
    service = UserService(db)
    await service.create_user(user_data)
    return {"detail": "Registered successfully"}


@router.post(
    "/token", status_code=status.HTTP_200_OK, response_model=TokenRead
)
async def get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = TokenService(db)
    return await service.get_access_token(form_data)


@router.get(
    "/profile", status_code=status.HTTP_200_OK, response_model=UserRead
)
async def profile(
    user_data: Annotated[dict[str, Any], Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = UserService(db)
    return await service.get_user(id=user_data["user_id"])


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[dict[str, Any], Depends(get_current_user)],
    pass_data: PasswordChange
):
    service = UserService(db)
    await service.change_password(user_data["user_id"], pass_data)
