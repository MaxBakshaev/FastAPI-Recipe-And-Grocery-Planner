from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ProductInfo(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    calories_per_gram: Optional[float] = Field(None, ge=0)


class ProductInRecipe(BaseModel):
    product_id: int
    quantity: int
    calories_per_gram: float


class RecipeCreateRequest(BaseModel):
    title: str
    body: str
    image_url: Optional[str] = None
    products_info: List[ProductInfo]


class RecipeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    body: str
    image_url: Optional[str] = None
    user_id: int
    products: List[ProductInRecipe]
    total_calories: int
    total_quantity: int


class RecipeUpdateRequest(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    image_url: Optional[str] = None
    products_info: Optional[List[ProductInfo]] = None
