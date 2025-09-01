from typing import Annotated

from fastapi import APIRouter, Depends, Request

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from crud.users import get_user_info
from utils.templates import templates

router = APIRouter(
    prefix="/profile",
    tags=["Users"],
)


@router.get("/", name="profile")
async def profile_page(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="profile/profile.html",
        context={
            "title": "Профиль",
        },
    )
