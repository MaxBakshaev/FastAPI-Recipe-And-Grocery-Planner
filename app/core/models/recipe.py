from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .mixins.id_int_pk import IdIntPkMixin

from . import Base

if TYPE_CHECKING:
    from .user import User
    from .product import Product
    from .recipe_product_association import RecipeProductAssociation


class Recipe(Base, IdIntPkMixin):

    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    image_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        default=None
    )
    product_associations: Mapped[list["RecipeProductAssociation"]] = relationship(
        "RecipeProductAssociation",
        back_populates="recipe",
        cascade="all, delete-orphan",
    )
    products: Mapped[list["Product"]] = relationship(
        secondary="recipe_product_association",
        viewonly=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        # nullable=False,
    )
    user: Mapped["User"] = relationship(back_populates="recipes")

    @property
    def total_quantity(self) -> int:
        """Возвращает суммарное количество (в граммах) всех продуктов"""
        return int(
            sum(assoc.quantity for assoc in self.product_associations),
        )

    @property
    def total_calories(self) -> int:
        """Возвращает общую калорийность рецепта"""
        return int(
            sum(assoc.total_calories for assoc in self.product_associations),
        )
