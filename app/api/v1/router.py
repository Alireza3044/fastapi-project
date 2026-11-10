from fastapi import APIRouter

from app.api.v1.endpoints import admin, auth, todo
from app.core.config import get_settings

settings = get_settings()

api_router = APIRouter(prefix=settings.API_V1_PREFIX)

api_router.include_router(admin.router)
api_router.include_router(auth.router)
api_router.include_router(todo.router)
