from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Product
from core.schemas.product import ProductCreate, ProductUpdate


async def get_products(session: AsyncSession) -> list[Product]:
    """Возвращает все продукты"""
    stmt = select(Product).order_by(Product.name)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product(
    session: AsyncSession,
    product_id: int,
) -> Product | None:
    """Возвращает продукт по id"""
    return await session.get(Product, product_id)


async def create_product(
    session: AsyncSession,
    product_in: ProductCreate,
) -> Product:
    """Возвращает созданный продукт"""
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    return product


async def update_product(
    session: AsyncSession,
    product: Product,
    product_update: ProductUpdate,
) -> Product:
    """Обновляет продукт"""
    for name, value in product_update.model_dump().items():
        setattr(product, name, value)
    await session.commit()
    return product


async def delete_product(
    session: AsyncSession,
    product: Product,
) -> None:
    """Удаляет продукт"""
    await session.delete(product)
    await session.commit()
