from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_v1.fastapi_users import current_active_user_bearer
from app.core.models import db_helper, Recipe, User
from app.utils.templates import templates

router = APIRouter(tags=["Views"])


@router.get("/", response_class=HTMLResponse, name="home")
async def index_page(request: Request):
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


@router.get("/profile_info")
async def api_profile(
    user=Depends(current_active_user_bearer),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    result = await session.execute(
        select(User)
        .options(
            selectinload(User.recipes).selectinload(
                Recipe.product_associations,
            ),
        )
        .where(User.id == user.id)
    )
    db_user = result.scalar_one()

    return {
        "id": str(db_user.id),
        "email": db_user.email,
        "username": db_user.username,
        "recipes": [
            {
                "id": recipe.id,
                "title": recipe.title,
                "body": recipe.body,
                "image_url": recipe.image_url,
                "total_quantity": recipe.total_quantity,
                "total_calories": recipe.total_calories,
            }
            for recipe in db_user.recipes
        ],
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


@router.get("/planner", response_class=HTMLResponse, name="planner")
async def planner_page(request: Request):
    return templates.TemplateResponse(
        "planner.html",
        {
            "request": request,
            "title": "Планировщик",
        },
    )
