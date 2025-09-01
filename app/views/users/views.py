from fastapi import APIRouter, Request
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
