import os
import uuid
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.fastapi_users import current_active_user_bearer
from api.api_v1.mixins import map_recipe_to_response
from crud import recipes
from core.config import settings
from core.models import db_helper, User
from core.schemas import (
    RecipeCreateRequest,
    RecipeResponse,
    RecipeUpdateRequest,
)

router = APIRouter(
    prefix=settings.api.v1.recipes,
    tags=["Recipes"],
)


@router.get("/", response_model=List[RecipeResponse])
async def get_recipes_with_products(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Возвращает список рецептов с продуктами"""
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
    """Создает и возвращает рецепт с продуктами"""
    try:
        recipe = await recipes.create_recipe_with_products(
            session=session,
            title=recipe_data.title,
            body=recipe_data.body,
            image_url=recipe_data.image_url,
            user_id=current_user.id,
            products_info=recipe_data.products_info,
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
            image_url=recipe_data.image_url,
            user_id=current_user.id,
            products_info=[
                (p.product_id, p.quantity, p.calories_per_gram)
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
    """Частично обновляет рецепт по id"""
    try:
        updated_recipe = await recipes.partial_update_recipe_with_products(
            session=session,
            recipe_id=recipe_id,
            user_id=current_user.id,
            title=recipe_data.title,
            body=recipe_data.body,
            image_url=recipe_data.image_url,
            products_info=(
                [
                    (p.product_id, p.quantity, p.calories_per_gram or 0.0)
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


@router.delete(
    "/{recipe_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_recipe(
    recipe_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: User = Depends(current_active_user_bearer),
):
    """Удаляет рецепт по id"""
    try:
        await recipes.delete_recipe(
            session=session,
            recipe_id=recipe_id,
            user_id=current_user.id,
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


os.makedirs("static/uploads/recipes", exist_ok=True)


@router.post("/upload/recipe-image")
async def upload_recipe_image(file: UploadFile = File(...)):
    # Проверяем тип файла
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Файл должен быть изображением",
        )

    # Проверяем размер файла (максимум 5MB)
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="Файл слишком большой. Максимальный размер: 5MB",
        )

    # Генерируем уникальное имя файла
    file_extension = (
        file.filename.split(".")[-1] if "." in file.filename else "jpg"
    )  # noqa: E501
    filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = f"static/uploads/recipes/{filename}"

    try:
        # Сохраняем файл
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Возвращаем URL для доступа к файлу
        image_url = f"/static/uploads/recipes/{filename}"
        return {"image_url": image_url}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при сохранении файла: {str(e)}"
        )
