"""https://fastapi-users.github.io/fastapi-users/latest/configuration/schemas/"""

from fastapi_users import schemas

from app.core.types.user_id import UserIdType


class UserRead(schemas.BaseUser[UserIdType]):
    pass


class UserCreate(schemas.BaseUserCreate):
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    pass
