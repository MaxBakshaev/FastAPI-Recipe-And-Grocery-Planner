from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from crud import products
from core.models import db_helper
from core.schemas import Product, ProductCreate, ProductUpdate
from core.config import settings

router = APIRouter(
    prefix=settings.api.v1.products,
    tags=["Products"],
)


@router.get("/", response_model=list[Product])
async def get_products(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Получение списка продуктов"""
    return await products.get_products(session=session)


@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Создание продукта"""
    return await products.create_product(
        session=session,
        product_in=product_in,
    )


@router.get("/{product_id}/", response_model=Product)
async def get_product_by_id(
    product_id: int = Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Product:
    """Получение продукта по id"""
    product = await products.get_product(
        session=session,
        product_id=product_id,
    )
    if product is not None:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Продукт {product_id} не найден!",
    )


@router.put("/{product_id}/")
async def update_product(
    product_update: ProductUpdate,
    product: Product = Depends(get_product_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Обновление продукта"""
    return await products.update_product(
        session=session,
        product=product,
        product_update=product_update,
    )


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: Product = Depends(get_product_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    """Удаление продукта по id"""
    await products.delete_product(session=session, product=product)
