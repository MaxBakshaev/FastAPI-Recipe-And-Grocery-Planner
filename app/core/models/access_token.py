from fastapi import Depends
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTable,
)

from sqlalchemy.ext.asyncio import AsyncSession

from core.types.user_id import UserIdType

from .base import Base


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable[UserIdType]):
    pass


async def get_access_token_db(
    session: AsyncSession = Depends(get_async_session),
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
