from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .mixins.id_int_pk import IdIntPkMixin

from . import Base


class User(IdIntPkMixin, Base):
    """Пользователь с id"""

    username: Mapped[str] = mapped_column(unique=True)
    foo: Mapped[int]
    bar: Mapped[int]

    __table_args__ = (
        UniqueConstraint(
            "foo",
            "bar",
        ),
    )
