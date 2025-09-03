from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from core.types.user_id import UserIdType
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from core.models import Profile


class User(Base, IdIntPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    """Пользователь с id, почтой, хеш-паролем"""

    username: Mapped[str] = mapped_column(String(32), unique=True)
    profile: Mapped["Profile"] = relationship("Profile", back_populates="user")
    
    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
