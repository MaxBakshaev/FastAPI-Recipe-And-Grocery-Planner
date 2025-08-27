from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from . import Base


class User(Base):
    """Пользователь с id"""

    username: Mapped[str] = mapped_column(unique=True)
