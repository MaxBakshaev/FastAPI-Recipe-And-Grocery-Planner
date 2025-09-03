from typing import Optional
from fastapi import APIRouter, Depends, Request

from api.api_v1.fastapi_users import optional_current_user_cookie
from core.models import User
from utils.templates import templates

from .users.views import router as users_router

router = APIRouter()


@router.get("/", name="home")
def index_page(
    request: Request,
    user: Optional[User] = Depends(optional_current_user_cookie),
):
    """https://fastapi.tiangolo.com/advanced/templates/#using-jinja2templates"""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "user": user,
            "title": "Главная",
        },
    )


router.include_router(users_router)
