from typing import Annotated
from uuid import UUID

from fastapi import Header
from jose import jwt

from app.core.environment import envs
from app.exceptions.authentication_error import AuthenticationError


def get_tenant_id_from_token(
    authorization: Annotated[str | None, Header()] = None,
) -> UUID:
    if not authorization:
        raise AuthenticationError

    if not authorization.startswith("Bearer "):
        raise AuthenticationError

    authorization = authorization.removeprefix("Bearer ").strip()
    if not authorization:
        raise AuthenticationError

    try:
        payload = jwt.decode(authorization, envs.JWT_SECRET, algorithms=["HS256"])
        if payload.get("type") != "tenant":
            raise AuthenticationError
        return UUID(payload["sub"])
    except AuthenticationError:
        raise
    except Exception as e:
        raise AuthenticationError from e
