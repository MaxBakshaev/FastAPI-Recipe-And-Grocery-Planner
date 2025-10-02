from typing import List, Optional, Tuple

from sqlalchemy import Result, select, delete
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

    associations = [
        RecipeProductAssociation(
            recipe_id=recipe.id,
            product_id=product_id,
            quantity=quantity,
            calories_per_unit=calories_per_unit,
        )
        for product_id, quantity, calories_per_unit in products_info
    ]
    session.add_all(associations)
    await session.commit()

    result = await session.execute(
        select(Recipe)
        .options(selectinload(Recipe.product_associations))
        .where(Recipe.id == recipe.id)
    )
    recipe = result.scalar_one()

    return recipe


async def get_recipe_with_products_by_id(
    session: AsyncSession, recipe_id: int
) -> Recipe | None:
    """Возвращает рецепт по id с продуктами"""
    stmt = (
        select(Recipe)
        .options(selectinload(Recipe.product_associations))
        .where(Recipe.id == recipe_id)
    )
    result: Result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def update_recipe_with_products(
    session: AsyncSession,
    recipe_id: int,
    title: str,
    body: str,
    user_id: int,
    products_info: List[Tuple[int, int, int]],
) -> Recipe:
    """
    Обновляет рецепт и связанные продукты.

    products_info — список кортежей:
    (product_id, quantity, calories_per_unit)
    """

    result = await session.execute(
        select(Recipe)
        .options(selectinload(Recipe.product_associations))
        .where(Recipe.id == recipe_id)
    )
    recipe = result.scalar_one_or_none()

    if recipe is None:
        raise ValueError("Recipe not found")

    if recipe.user_id != user_id:
        raise PermissionError("Not allowed to update this recipe")

    recipe.title = title
    recipe.body = body

    await session.execute(
        delete(RecipeProductAssociation).where(
            RecipeProductAssociation.recipe_id == recipe_id
        )
    )

    associations = [
        RecipeProductAssociation(
            recipe_id=recipe_id,
            product_id=product_id,
            quantity=quantity,
            calories_per_unit=calories_per_unit,
        )
        for product_id, quantity, calories_per_unit in products_info
    ]
    session.add_all(associations)

    await session.commit()

    result = await session.execute(
        select(Recipe)
        .options(selectinload(Recipe.product_associations))
        .where(Recipe.id == recipe_id)
    )
    updated_recipe = result.scalar_one()

    return updated_recipe


async def partial_update_recipe_with_products(
    session: AsyncSession,
    recipe_id: int,
    user_id: int,
    title: Optional[str] = None,
    body: Optional[str] = None,
    products_info: Optional[List[Tuple[int, int, int]]] = None,
) -> Recipe:
    """Частичто обновляет рецепт"""
    result = await session.execute(
        select(Recipe)
        .options(selectinload(Recipe.product_associations))
        .where(Recipe.id == recipe_id)
    )
    recipe = result.scalar_one_or_none()
    if recipe is None:
        raise ValueError("Recipe not found")

    if recipe.user_id != user_id:
        raise PermissionError("Not allowed to update this recipe")

    if title is not None:
        recipe.title = title
    if body is not None:
        recipe.body = body

    if products_info is not None:
        await session.execute(
            delete(RecipeProductAssociation).where(
                RecipeProductAssociation.recipe_id == recipe_id
            )
        )
        associations = [
            RecipeProductAssociation(
                recipe_id=recipe_id,
                product_id=product_id,
                quantity=quantity,
                calories_per_unit=calories_per_unit,
            )
            for product_id, quantity, calories_per_unit in products_info
        ]
        session.add_all(associations)

    await session.commit()

    result = await session.execute(
        select(Recipe)
        .options(selectinload(Recipe.product_associations))
        .where(Recipe.id == recipe_id)
    )
    return result.scalar_one()


async def delete_recipe(
    session: AsyncSession,
    recipe_id: int,
    user_id: int,
) -> None:
    """
    Удаляет рецепт и связанные с ним продукты.

    Проверяет, что рецепт принадлежит user_id.
    """

    result = await session.execute(select(Recipe).where(Recipe.id == recipe_id))
    recipe = result.scalar_one_or_none()
    if recipe is None:
        raise ValueError("Recipe not found")

    if recipe.user_id != user_id:
        raise PermissionError("Not allowed to delete this recipe")

    await session.execute(
        delete(RecipeProductAssociation).where(
            RecipeProductAssociation.recipe_id == recipe_id
        )
    )

    await session.execute(delete(Recipe).where(Recipe.id == recipe_id))
    await session.commit()
