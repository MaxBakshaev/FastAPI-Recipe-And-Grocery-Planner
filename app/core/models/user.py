from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
)

from .mixins.id_int_pk import IdIntPkMixin

from . import Base


class User(Base, IdIntPkMixin, SQLAlchemyBaseUserTable[int]):
    """Пользователь с id"""
    pass
