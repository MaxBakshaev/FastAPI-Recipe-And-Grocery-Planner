from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from app.core.config import settings

from .auth import router as auth_router
from .users import router as users_router
from .messages import router as messages_router
from .products import router as products_router
from .recipes import router as recipes_router
from .saved_recipes import router as saved_recipes_router

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.v1.prefix,
    dependencies=[Depends(http_bearer)],
)

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(messages_router)
router.include_router(products_router)
router.include_router(recipes_router)
router.include_router(saved_recipes_router)
