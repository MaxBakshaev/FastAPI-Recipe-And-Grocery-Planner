from typing import TYPE_CHECKING

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .mixins.id_int_pk import IdIntPkMixin

from . import Base


if TYPE_CHECKING:
    from .recipe import Recipe
    from .recipe_product_association import RecipeProductAssociation


class Product(Base, IdIntPkMixin):

    name: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    calories_per_gram: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        server_default="0",
    )

    recipe_associations: Mapped[list["RecipeProductAssociation"]] = relationship(
        "RecipeProductAssociation",
        back_populates="product",
        cascade="all, delete-orphan",
    )
    recipes: Mapped[list["Recipe"]] = relationship(
        secondary="recipe_product_association",
        viewonly=True,
    )
