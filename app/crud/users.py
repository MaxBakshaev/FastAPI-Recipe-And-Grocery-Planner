from typing import Sequence

from fastapi_users.exceptions import InvalidPasswordException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.authentication import UserManager
from app.core.schemas import UserCreate
from app.core.models import User, Profile


async def get_all_users(
    session: AsyncSession,
) -> Sequence[User]:
    """Возвращает список всех пользователей"""
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_user(
    session: AsyncSession,
    user_create: UserCreate,
) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    # await session.refresh(user)
    return user


async def get_user_info(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    return await session.get(User, user_id)


async def authenticate_user(
    email: str,
    password: str,
    user_manager: UserManager,
):
    user = await user_manager.get_by_email(email)
    if not user:
        return None
    try:
        await user_manager.validate_password(password, user)
    except InvalidPasswordException:
        return None
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    """Создать профиль пользователя"""
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(profile)
    await session.commit()
    return profile
