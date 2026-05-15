from collections.abc import Callable
from typing import Annotated

from fastapi import Header

from app.exceptions.authentication_error import AuthenticationError
from app.exceptions.authorization_error import AuthorizationError
from app.utils.jwt import decode


def _extract_bearer_token(authorization: str | None) -> str:
    if not authorization:
        raise AuthenticationError

    if not authorization.startswith("Bearer "):
        raise AuthenticationError

    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise AuthenticationError
    return token


def _decode_payload(authorization: str | None) -> dict:
    token = _extract_bearer_token(authorization)
    try:
        payload = decode(token)
    except Exception as exc:
        raise AuthenticationError from exc

    if not isinstance(payload, dict):
        raise AuthenticationError
    return payload


def _get_permission_codes(payload: dict) -> set[str]:
    role = payload.get("role")
    if not isinstance(role, dict):
        return set()

    permissions = role.get("permissions")
    if not isinstance(permissions, list):
        return set()

    codes: set[str] = set()
    for permission in permissions:
        if isinstance(permission, dict) and isinstance(permission.get("code"), str):
            codes.add(permission["code"])
        elif isinstance(permission, str):
            codes.add(permission)
    return codes


def verify_user_jwt(authorization: Annotated[str | None, Header()] = None) -> None:
    payload = _decode_payload(authorization)
    if payload.get("type") != "user":
        raise AuthenticationError


def verify_tenant_jwt(authorization: Annotated[str | None, Header()] = None) -> None:
    payload = _decode_payload(authorization)
    if payload.get("type") != "tenant":
        raise AuthenticationError


def require_permission(permission_code: str) -> Callable[..., None]:
    def dependency(authorization: Annotated[str | None, Header()] = None) -> None:
        payload = _decode_payload(authorization)
        if payload.get("type") != "tenant":
            raise AuthenticationError

        permission_codes = _get_permission_codes(payload)
        if permission_code not in permission_codes:
            message = f"Permissão necessária: {permission_code}"
            raise AuthorizationError(message)

    return dependency


def require_any_permission(permission_codes: list[str]) -> Callable[..., None]:
    def dependency(authorization: Annotated[str | None, Header()] = None) -> None:
        payload = _decode_payload(authorization)
        if payload.get("type") != "tenant":
            raise AuthenticationError

        current_permission_codes = _get_permission_codes(payload)
        if not any(code in current_permission_codes for code in permission_codes):
            message = "Permissão insuficiente para acessar este recurso"
            raise AuthorizationError(message)

    return dependency
