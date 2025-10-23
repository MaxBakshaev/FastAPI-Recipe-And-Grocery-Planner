from typing import Annotated
from fastapi import APIRouter, Depends

from app.api.api_v1.fastapi_users import (
    current_active_user_bearer,
    current_active_super_user_bearer,
)
from app.core.config import settings
from app.core.models import User
from app.core.schemas import UserRead

router = APIRouter(
    prefix=settings.api.v1.messages,
    tags=["Messages"],
)


@router.get("")
def get_user_messages(
    user: Annotated[
        User,
        Depends(current_active_user_bearer),
    ],
):
    return {
        "messages": ["m1", "m2", "m3"],
        "user": UserRead.model_validate(user),
    }


@router.get("/secrets")
def get_superuser_messages(
    user: Annotated[
        User,
        Depends(current_active_super_user_bearer),
    ],
):
    return {
        "messages": ["secret-m1", "secret-m2", "secret-m3"],
        "user": UserRead.model_validate(user),
    }
