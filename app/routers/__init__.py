from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.club import router as club_router
from app.routers.activity import router as activity_router

__all__ = [
    "health_router",
    "auth_router",
    "users_router",
    "club_router",
    "activity_router",
]
