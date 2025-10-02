from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.api_v1.fastapi_users import current_active_user_bearer
from api.api_v1.mixins import map_recipe_to_response
from crud import recipes
from core.models import db_helper, User, Recipe
from core.schemas.recipe import RecipeCreateRequest, RecipeResponse
from core.config import settings

router = APIRouter(
    prefix=settings.api.v1.recipes,
    tags=["Recipes"],
)


@router.get("/", response_model=List[RecipeResponse])
async def get_recipes_with_products(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получение списка рецептов с продуктами"""
    recipe_list = await recipes.get_recipes_with_products(session=session)

    return [map_recipe_to_response(recipe) for recipe in recipe_list]


@router.post(
    "/",
    response_model=RecipeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_recipe_with_products(
    recipe_data: RecipeCreateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(current_active_user_bearer),
):
    """Возвращает все рецепты с продуктами"""
    try:
        recipe = await recipes.create_recipe_with_products(
            session=session,
            title=recipe_data.title,
            body=recipe_data.body,
            user_id=current_user.id,
            products_info=[
                (p.product_id, p.quantity, p.calories_per_unit)
                for p in recipe_data.products_info
            ],
        )
        result = await session.execute(
            select(Recipe)
            .options(selectinload(Recipe.product_associations))
            .where(Recipe.id == recipe.id)
        )
        recipe = result.scalar_one()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return map_recipe_to_response(recipe)
