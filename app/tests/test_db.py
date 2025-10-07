import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper


@pytest.mark.asyncio
async def test_create_session():
    """Проверяет, что метод session_getter у объекта db_helper
    создает и возвращает асинхронную сессию.
    """
    async for session in db_helper.session_getter():
        assert isinstance(session, AsyncSession)
