"""https://fastapi-users.github.io/fastapi-users/latest/configuration/authentication/transports/bearer/"""

from fastapi_users.authentication import BearerTransport, CookieTransport

from core.config import settings

cookie_transport = CookieTransport(
    cookie_name="access_token",
    cookie_max_age=3600,
    cookie_secure=False,
)


bearer_transport = BearerTransport(
    tokenUrl=settings.api.bearer_token_url,
)
