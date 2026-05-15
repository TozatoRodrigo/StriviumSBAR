from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.exceptions.authentication_error import AuthenticationError
from app.models.user import User
from app.modules.user.exceptions.user_not_found_error import UserNotFoundError
from app.services.cloudflare.turnstile import TurnstileService
from app.services.logged_user.logged_user_service import LoggedUserService
from app.services.token.user_token_service import UserTokenService


def get_turnstile_service() -> TurnstileService:
    return TurnstileService()


def get_user_token_service(
    authorization: Annotated[str | None, Header()] = None,
) -> UserTokenService:
    return UserTokenService(authorization or "")


def get_logged_user_service(
    session: Annotated[Session, Depends(get_session)],
    token_service: Annotated[UserTokenService, Depends(get_user_token_service)],
) -> LoggedUserService:
    return LoggedUserService(session, token_service)


def get_logged_user(
    logged_user_service: Annotated[LoggedUserService, Depends(get_logged_user_service)],
) -> User:
    user = logged_user_service.get_logged_user()
    if user is None:
        msg = "Usuário não encontrado ou não autenticado"
        raise UserNotFoundError(msg)
    return user


def get_user_id_from_token(
    user_token_service: Annotated[UserTokenService, Depends(get_user_token_service)],
) -> UUID:
    user_id = user_token_service.get_user_id_from_token()
    if user_id is None:
        raise AuthenticationError
    return UUID(user_id)


def get_user_id_from_tenant_token(
    user_token_service: Annotated[UserTokenService, Depends(get_user_token_service)],
) -> UUID:
    user_id = user_token_service.get_user_id_from_tenant_token()
    if user_id is None:
        raise AuthenticationError
    return UUID(user_id)


def get_logged_user_by_tenant_token(
    logged_user_service: Annotated[LoggedUserService, Depends(get_logged_user_service)],
) -> User | None:
    return logged_user_service.get_logged_user_by_tenant_token()
