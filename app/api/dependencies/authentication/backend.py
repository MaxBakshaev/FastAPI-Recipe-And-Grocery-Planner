"""https://fastapi-users.github.io/fastapi-users/latest/configuration/authentication/backend/"""

from fastapi_users.authentication import AuthenticationBackend

from .strategy import get_database_strategy
from core.authentication import bearer_transport, cookie_transport

authentication_backend_bearer = AuthenticationBackend(
    name="access-tokens-db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)

authentication_backend_cookie = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_database_strategy,
)
