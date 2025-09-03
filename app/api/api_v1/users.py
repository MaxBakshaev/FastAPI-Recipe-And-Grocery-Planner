"""https://fastapi-users.github.io/fastapi-users/latest/configuration/routers/users/"""

from fastapi import APIRouter

from core.schemas.user import UserRead, UserUpdate

from .fastapi_users import fastapi_users_bearer
from core.config import settings

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
)

# /me
# /{id}
router.include_router(
    router=fastapi_users_bearer.get_users_router(
        UserRead,
        UserUpdate,
    ),
)
