from typing import List, Tuple

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Recipe, RecipeProductAssociation


async def get_recipes_with_products(session: AsyncSession) -> list[Recipe]:
    """Возвращает все рецепты с продуктами"""
    stmt = (
        select(Recipe)
        .options(selectinload(Recipe.product_associations))
        .order_by(Recipe.id)
    )
    result: Result = await session.execute(stmt)
    recipes = result.scalars().all()
    return list(recipes)


async def create_recipe_with_products(
    session: AsyncSession,
    title: str,
    body: str,
    user_id: int,
    # [(product_id, quantity, calories_per_unit), ...]
    products_info: List[Tuple[int, int, int]],
) -> Recipe:
    """
    Создает рецепт и связывает с продуктами через RecipeProductAssociation.
    Возвращает рецепт с продуктами.

    products_info — список кортежей с информацией о продуктах:
    (product_id, quantity в граммах, calories_per_unit)
    """

    recipe = Recipe(title=title, body=body, user_id=user_id)
    session.add(recipe)
    await session.flush()  # получение recipe.id

    associations = []
    for product_id, quantity, calories_per_unit in products_info:
        assoc = RecipeProductAssociation(
            recipe_id=recipe.id,
            product_id=product_id,
            quantity=quantity,
            calories_per_unit=calories_per_unit,
        )
        associations.append(assoc)

    session.add_all(associations)
    await session.commit()

    await session.refresh(recipe)
    return recipe
