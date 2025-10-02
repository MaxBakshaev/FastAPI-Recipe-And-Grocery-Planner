from typing import List
from pydantic import BaseModel, ConfigDict, Field


class ProductInfo(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    calories_per_unit: int = Field(..., ge=0)


class ProductInRecipe(BaseModel):
    product_id: int
    quantity: int
    calories_per_unit: int


class RecipeCreateRequest(BaseModel):
    title: str
    body: str
    products_info: List[ProductInfo]


class RecipeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    body: str
    user_id: int
    products: List[ProductInRecipe]
