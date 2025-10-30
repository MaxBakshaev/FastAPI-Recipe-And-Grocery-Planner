from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_v1.fastapi_users import current_active_user_bearer
from app.api.api_v1.mixins import map_recipe_to_response
from app.crud import saved_recipes, recipes
from app.core.config import settings
from app.core.models import db_helper, User
from app.core.schemas import RecipeResponse, SaveRecipeRequest

router = APIRouter(
    prefix=settings.api.v1.saved_recipes,
    tags=["Saved Recipes"],
)


@router.get("/", response_model=List[RecipeResponse])
async def get_my_saved_recipes(
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(current_active_user_bearer),
):
    """Возвращает сохраненные рецепты текущего пользователя"""

    saved_recipes_list = await saved_recipes.get_saved_recipes(
        session=session,
        user_id=current_user.id,
    )

    return [
        map_recipe_to_response(saved_recipe.recipe)
        for saved_recipe in saved_recipes_list
    ]


@router.post(
    "/",
    response_model=RecipeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def save_recipe(
    save_request: SaveRecipeRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(current_active_user_bearer),
):
    """Сохраняет рецепт для текущего пользователя"""

    try:
        await saved_recipes.save_recipe(
            session=session,
            user_id=current_user.id,
            recipe_id=save_request.recipe_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Получаем полную информацию о рецепте
    recipe = await recipes.get_recipe_with_products_by_id(
        session=session,
        recipe_id=save_request.recipe_id,
    )

    return map_recipe_to_response(recipe)


@router.delete(
    "/{recipe_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unsave_recipe(
    recipe_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(current_active_user_bearer),
):
    """Удаляет рецепт из сохраненных"""

    try:
        await saved_recipes.unsave_recipe(
            session=session,
            user_id=current_user.id,
            recipe_id=recipe_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/check/{recipe_id}/")
async def check_recipe_saved(
    recipe_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(current_active_user_bearer),
):
    """Проверяет, сохранен ли рецепт пользователем"""

    is_saved = await saved_recipes.is_recipe_saved_by_user(
        session=session,
        user_id=current_user.id,
        recipe_id=recipe_id,
    )

    return {"is_saved": is_saved}
