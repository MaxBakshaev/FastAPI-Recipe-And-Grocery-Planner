from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):

    name: str


class ProductCreate(ProductBase):
    """Создание нового продукта"""

    pass


class ProductUpdate(ProductCreate):
    """Обновление продукта"""

    pass


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
