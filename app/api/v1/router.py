from fastapi import APIRouter

from app.api.v1.endpoints import admin, auth, todo
from app.core.config import get_settings

settings = get_settings()

api_router = APIRouter()

api_router.include_router(admin.router, prefix="/admin")
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(todo.router, prefix="/todo")
