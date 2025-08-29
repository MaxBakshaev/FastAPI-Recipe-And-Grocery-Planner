"""
https://fastapi-users.github.io/fastapi-users/latest/configuration/routers/auth/
https://fastapi-users.github.io/fastapi-users/latest/configuration/routers/register/
"""

from fastapi import APIRouter

from core.schemas.user import UserCreate, UserRead

from .fastapi_users import fastapi_users
from api.dependencies.authentication.backend import authentication_backend
from core.config import settings

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["auth"],
)

# /login
# /logout
router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
    ),
)

# /register
router.include_router(
    fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)
