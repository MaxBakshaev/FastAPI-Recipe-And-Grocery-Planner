from typing import List, Sequence

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.models import SavedRecipe, Recipe


async def get_saved_recipes(
    session: AsyncSession,
    user_id: int,
) -> Sequence[SavedRecipe]:
    """Возвращает сохраненные рецепты пользователя"""

    stmt = (
        select(SavedRecipe)
        .options(
            selectinload(SavedRecipe.recipe).selectinload(
                Recipe.product_associations,
            )
        )
        .where(SavedRecipe.user_id == user_id)
        .order_by(SavedRecipe.id)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def save_recipe(
    session: AsyncSession,
    user_id: int,
    recipe_id: int,
) -> SavedRecipe:
    """Сохраняет рецепт для пользователя"""

    # Проверка существует ли рецепт
    recipe = await session.get(Recipe, recipe_id)
    if not recipe:
        raise ValueError("Recipe not found")

    # Проверка не сохранен ли уже рецепт
    existing_saved = await session.execute(
        select(SavedRecipe).where(
            SavedRecipe.user_id == user_id,
            SavedRecipe.recipe_id == recipe_id,
        )
    )
    if existing_saved.scalar_one_or_none():
        raise ValueError("Recipe already saved")

    saved_recipe = SavedRecipe(
        user_id=user_id,
        recipe_id=recipe_id,
    )
    session.add(saved_recipe)
    await session.commit()
    await session.refresh(saved_recipe)

    return saved_recipe


async def unsave_recipe(
    session: AsyncSession,
    user_id: int,
    recipe_id: int,
) -> None:
    """Удаляет рецепт из сохраненных"""

    await session.execute(
        delete(SavedRecipe).where(
            SavedRecipe.user_id == user_id,
            SavedRecipe.recipe_id == recipe_id,
        )
    )
    await session.commit()


async def is_recipe_saved_by_user(
    session: AsyncSession,
    user_id: int,
    recipe_id: int,
) -> bool:
    """Проверяет, сохранен ли рецепт пользователем"""

    stmt = select(SavedRecipe).where(
        SavedRecipe.user_id == user_id,
        SavedRecipe.recipe_id == recipe_id,
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none() is not None


async def get_saved_recipe_ids(
    session: AsyncSession,
    user_id: int,
) -> List[int]:
    """Возвращает список ID сохраненных рецептов пользователя"""

    stmt = select(SavedRecipe.recipe_id).where(
        SavedRecipe.user_id == user_id,
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())
