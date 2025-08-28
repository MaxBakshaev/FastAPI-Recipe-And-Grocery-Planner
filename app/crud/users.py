from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.user import UserCreate
from core.models import User

from passlib.context import CryptContext


async def get_all_users(
    session: AsyncSession,
) -> Sequence[User]:
    """Возвращает список всех пользователей"""
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


def get_password_hash(password: str) -> str:
    """Возвращает хешированный пароль"""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


async def create_user(
    session: AsyncSession,
    user_create: UserCreate,
) -> User:

    hashed_password = get_password_hash(user_create.password)

    user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password,
    )

    session.add(user)
    await session.commit()
    # await session.refresh(user)
    return user
