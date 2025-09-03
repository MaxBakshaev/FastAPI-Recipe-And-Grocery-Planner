from fastapi_users import FastAPIUsers

from core.models import User
from core.types.user_id import UserIdType

from api.dependencies.authentication import get_user_manager
from api.dependencies.authentication import authentication_backend_bearer, authentication_backend_cookie

fastapi_users_bearer = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [authentication_backend_bearer],
)

fastapi_users_cookie = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [authentication_backend_cookie],
)

current_active_user_bearer = fastapi_users_bearer.current_user(active=True)
current_active_super_user_bearer = fastapi_users_bearer.current_user(active=True, superuser=True)
optional_current_user_bearer = fastapi_users_bearer.current_user(optional=True)

current_active_user_cookie = fastapi_users_cookie.current_user(active=True)
current_active_super_user_cookie = fastapi_users_cookie.current_user(active=True, superuser=True)
optional_current_user_cookie = fastapi_users_cookie.current_user(optional=True)
