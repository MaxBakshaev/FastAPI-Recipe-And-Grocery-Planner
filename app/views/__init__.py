from fastapi import APIRouter, Request

from utils.templates import templates

from .users.views import router as users_router

router = APIRouter()


@router.get("/", name="home")
def index_page(
    request: Request,
):
    """https://fastapi.tiangolo.com/advanced/templates/#using-jinja2templates"""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "Главная",
        },
    )


router.include_router(users_router)
