from uuid import UUID

from jose import jwt

from app.core.environment import envs
from app.modules.auth.dtos.responses.auth.default_auth_response_dto import (
    DefaultAuthResponseDTO,
)
from app.modules.auth.exceptions.refresh_auth_error import RefreshAuthError
from app.modules.auth.services.refresh_token.refresh_token_service import (
    RefreshTokenService,
)
from app.modules.auth.services.user.user_service import UserService
from app.modules.auth.use_cases.auth.default_auth_use_case import DefaultAuthUseCase
from app.modules.auth.utils.jwt import (
    REFRESH_TOKEN_EXPIRES_MINUTES,
    generate_refresh_token,
)
from app.modules.user.exceptions.user_not_found_error import UserNotFoundError


class RefreshUserAuthUseCase:
    def __init__(
        self, user_service: UserService, refresh_token_service: RefreshTokenService
    ) -> None:
        self.user_service = user_service
        self.refresh_token_service = refresh_token_service

    def handle(self, refresh_token: str) -> DefaultAuthResponseDTO:
        payload = self.__decode_refresh_token(refresh_token)
        if payload.get("type") != "user-refresh":
            raise RefreshAuthError

        try:
            user_id = UUID(payload["sub"])
        except (KeyError, TypeError, ValueError) as e:
            raise RefreshAuthError from e

        user = self.user_service.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError

        try:
            jti = UUID(jti_claim) if (jti_claim := payload.get("jti")) else None
        except (TypeError, ValueError) as e:
            raise RefreshAuthError from e

        new_jti, _token_family = self.refresh_token_service.validate_and_rotate(
            jti=jti,
            user_id=user_id,
            token_type="user-refresh",  # noqa: S106
            expires_minutes=REFRESH_TOKEN_EXPIRES_MINUTES,
        )

        access_token = DefaultAuthUseCase.get_access_token(user)
        new_refresh = generate_refresh_token(
            {"sub": str(user.id), "type": "user-refresh"}, jti=new_jti
        )

        return DefaultAuthResponseDTO(
            access_token=access_token,
            refresh_token=new_refresh,
            token_type="Bearer",  # noqa: S106
            expires_in=120,
        )

    @staticmethod
    def __decode_refresh_token(refresh_token: str) -> dict:
        try:
            return jwt.decode(refresh_token, envs.JWT_SECRET, algorithms=["HS256"])
        except Exception as e:
            raise RefreshAuthError from e
