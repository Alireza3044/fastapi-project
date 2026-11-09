from .todo import router as todo_router
from .user import router as user_router
from .admin import router as admin_router

__all__ = ["todo_router", "user_router", "admin_router"]
