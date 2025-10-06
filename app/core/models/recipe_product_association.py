from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

if TYPE_CHECKING:
    from .recipe import Recipe
    from .product import Product


class RecipeProductAssociation(Base):

    __tablename__ = "recipe_product_association"
    __table_args__ = (
        UniqueConstraint("recipe_id", "product_id", name="uq_recipe_product"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    # граммовка
    quantity: Mapped[int] = mapped_column(
        default="0",
        server_default="0",
    )
    # калории на грамм
    calories_per_unit: Mapped[float] = mapped_column(
        default=0.0,
        server_default="0",
    )

    recipe: Mapped["Recipe"] = relationship(back_populates="product_associations")
    product: Mapped["Product"] = relationship(back_populates="recipe_associations")

    @property
    def total_calories(self) -> int:
        """Возвращает общую калорийность рецепта"""
        return self.quantity * self.calories_per_unit
