from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import authenticate_user, generate_access_token


class TokenService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_access_token(
        self,
        form_data: OAuth2PasswordRequestForm
    ) -> dict[str, str]:
        user = await authenticate_user(
            form_data.username, form_data.password, self.db
        )

        token = await generate_access_token(
            user.id,  # type: ignore
            user.username,  # type: ignore
            user.role,  # type: ignore
            timedelta(minutes=20)
        )
        return {"access_token": token, "token_type": "bearer"}
