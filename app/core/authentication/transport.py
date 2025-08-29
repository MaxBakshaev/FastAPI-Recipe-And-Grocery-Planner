"""https://fastapi-users.github.io/fastapi-users/latest/configuration/authentication/transports/bearer/"""

from fastapi_users.authentication import BearerTransport

bearer_transport = BearerTransport(
    tokenUrl="auth/jwt/login",
)
