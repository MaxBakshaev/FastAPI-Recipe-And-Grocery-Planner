from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from app.core.models import db_helper, AccessToken

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_tokens_db(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    """https://fastapi-users.github.io/fastapi-users/latest/configuration/authentication/strategies/database/"""
    yield AccessToken.get_db(session=session)
