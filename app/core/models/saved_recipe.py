from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

if TYPE_CHECKING:
    from .user import User
    from .recipe import Recipe


class SavedRecipe(Base):
    __tablename__ = "saved_recipes"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "recipe_id",
            name="uq_user_recipe",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))

    user: Mapped["User"] = relationship(back_populates="saved_recipes")
    recipe: Mapped["Recipe"] = relationship(back_populates="saved_by_users")
