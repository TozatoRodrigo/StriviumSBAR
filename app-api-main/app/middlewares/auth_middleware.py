from typing import Annotated

from fastapi import Header

from app.exceptions.authentication_error import AuthenticationError
from app.utils.jwt import decode
from app.utils.jwt import verify as verify_jwt_token


def verify_user_jwt(authorization: Annotated[str | None, Header()]) -> None:
    if not authorization:
        raise AuthenticationError

    authorization = authorization.replace("Bearer ", "")
    if not verify_jwt_token(authorization):
        raise AuthenticationError


def verify_tenant_jwt(authorization: Annotated[str | None, Header()]) -> None:
    if not authorization:
        raise AuthenticationError

    authorization = authorization.replace("Bearer ", "")
    payload = decode(authorization)
    if not payload or payload["type"] != "tenant":
        raise AuthenticationError
