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
async def users_list(
    request: Request,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):

    user = await get_user_info(session=session, user_id=1)
    return templates.TemplateResponse(
        request=request,
        name="profile/profile.html",
        context={"user": user},
    )
