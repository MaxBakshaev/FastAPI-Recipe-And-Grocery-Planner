from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.fastapi_users import current_active_user_bearer
from api.api_v1.mixins import map_recipe_to_response
from crud import recipes
from core.models import db_helper, User
from core.schemas.recipe import (
    RecipeCreateRequest,
    RecipeResponse,
    RecipeUpdateRequest,
)
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

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return map_recipe_to_response(recipe)


@router.get("/{recipe_id}/", response_model=RecipeResponse)
async def get_recipe_with_products_by_id(
    recipe_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> RecipeResponse:
    """Возвращает рецепт по id с продуктами"""
    recipe = await recipes.get_recipe_with_products_by_id(
        session=session,
        recipe_id=recipe_id,
    )
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return map_recipe_to_response(recipe)


@router.put("/{recipe_id}/", response_model=RecipeResponse)
async def update_recipe_with_products(
    recipe_id: int,
    recipe_data: RecipeCreateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(current_active_user_bearer),
):
    """Обновляет рецепт по id с продуктами"""
    try:
        recipe = await recipes.update_recipe_with_products(
            session=session,
            recipe_id=recipe_id,
            title=recipe_data.title,
            body=recipe_data.body,
            user_id=current_user.id,
            products_info=[
                (p.product_id, p.quantity, p.calories_per_unit)
                for p in recipe_data.products_info
            ],
        )
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return map_recipe_to_response(recipe)


@router.patch("/{recipe_id}/", response_model=RecipeResponse)
async def partial_update_recipe(
    recipe_id: int,
    recipe_data: RecipeUpdateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(current_active_user_bearer),
):
    """Частичное обновление рецепта по id"""
    try:
        updated_recipe = await recipes.partial_update_recipe_with_products(
            session=session,
            recipe_id=recipe_id,
            user_id=current_user.id,
            title=recipe_data.title,
            body=recipe_data.body,
            products_info=(
                [
                    (p.product_id, p.quantity, p.calories_per_unit)
                    for p in recipe_data.products_info
                ]
                if recipe_data.products_info is not None
                else None
            ),
        )
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return map_recipe_to_response(updated_recipe)


@router.delete("/{recipe_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(
    recipe_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(current_active_user_bearer),
):
    """Удаление рецепта по id"""
    try:
        await recipes.delete_recipe(
            session=session, recipe_id=recipe_id, user_id=current_user.id
        )
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found",
        )
    except PermissionError:
        raise HTTPException(
            status_code=403,
            detail="Not allowed to delete this recipe",
        )
