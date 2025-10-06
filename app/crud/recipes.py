from typing import List, Optional, Tuple

from fastapi import HTTPException
from sqlalchemy import Result, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.schemas.recipe import ProductInfo
from core.models import Product, Recipe, RecipeProductAssociation


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
    products_info: List[ProductInfo],
) -> Recipe:
    """
    Создает рецепт и связывает с продуктами через RecipeProductAssociation.
    Автоматически подставляет calories_per_unit, если он не указан.
    """

    recipe = Recipe(title=title, body=body, user_id=user_id)
    session.add(recipe)
    await session.flush()  # Получаем recipe.id

    associations = []

    for product_info in products_info:
        # Если калории не указаны — достаём из базы
        if product_info.calories_per_unit is None:
            db_product = await session.get(Product, product_info.product_id)
            if not db_product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Продукт ID {product_info.product_id} не найден",
                )
            calories_per_unit = db_product.calories_per_unit
        else:
            calories_per_unit = product_info.calories_per_unit

        assoc = RecipeProductAssociation(
            recipe_id=recipe.id,
            product_id=product_info.product_id,
            quantity=product_info.quantity,
            calories_per_unit=calories_per_unit,
        )
        associations.append(assoc)

    session.add_all(associations)
    await session.commit()

    result = await session.execute(
        select(Recipe)
        .options(selectinload(Recipe.product_associations))
        .where(Recipe.id == recipe.id)
    )
    return result.scalar_one()


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
    products_info: List[Tuple[int, int, float]],
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
    products_info: Optional[List[Tuple[int, int, float]]] = None,
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
