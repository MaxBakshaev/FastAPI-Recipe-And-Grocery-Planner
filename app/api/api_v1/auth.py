"""
https://fastapi-users.github.io/fastapi-users/latest/configuration/routers/auth/
https://fastapi-users.github.io/fastapi-users/latest/configuration/routers/register/
https://fastapi-users.github.io/fastapi-users/latest/configuration/routers/verify/
https://fastapi-users.github.io/fastapi-users/latest/configuration/routers/reset/
"""

from fastapi import APIRouter

from app.core.schemas import UserCreate, UserRead

from .fastapi_users import fastapi_users_bearer
from app.api.dependencies.authentication import authentication_backend_bearer
from app.core.config import settings

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)

# /login
# /logout
router.include_router(
    router=fastapi_users_bearer.get_auth_router(
        authentication_backend_bearer,
        # requires_verification=True,
    ),
)

# /register
router.include_router(
    fastapi_users_bearer.get_register_router(
        UserRead,
        UserCreate,
    ),
)

# /request-verify-token
# /verify
router.include_router(
    router=fastapi_users_bearer.get_verify_router(UserRead),
)

# /forgot-password
# /reset-password
router.include_router(
    router=fastapi_users_bearer.get_reset_password_router(),
)
