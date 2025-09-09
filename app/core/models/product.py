from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .mixins.id_int_pk import IdIntPkMixin

from . import Base


class Product(Base, IdIntPkMixin):

    name: Mapped[str] = mapped_column(String(32), unique=True, index=True)
