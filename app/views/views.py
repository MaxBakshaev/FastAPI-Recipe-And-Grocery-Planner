from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from api.api_v1.fastapi_users import current_active_user_bearer
from utils.templates import templates

router = APIRouter(tags=["Views"])


@router.get("/", response_class=HTMLResponse, name="home")
async def index_page(request: Request):
    """https://fastapi.tiangolo.com/advanced/templates/#using-jinja2templates"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Главная",
        },
    )


@router.get("/login", response_class=HTMLResponse, name="login")
async def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "title": "Войти",
        },
    )


@router.get("/register", name="register")
async def register_page(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "title": "Регистрация",
        },
    )


@router.get("/profile", response_class=HTMLResponse, name="profile")
async def profile_page(request: Request):
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "title": "Профиль",
        },
    )


@router.get("/api/profile")
async def api_profile(
    user=Depends(current_active_user_bearer),
):
    # Защищённый API, который возвращает данные пользователя
    return {
        "id": str(user.id),
        "email": user.email,
        "username": user.username,
    }


@router.get("/recipes", response_class=HTMLResponse, name="recipe")
async def recipe(request: Request):
    return templates.TemplateResponse(
        "recipe.html",
        {
            "request": request,
            "title": "Рецепты",
        },
    )


@router.get("/api/me")
async def get_me(user=Depends(current_active_user_bearer)):
    return {
        "email": user.email,
        "id": str(user.id),
    }
