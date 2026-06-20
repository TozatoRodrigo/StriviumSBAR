from uuid import UUID

from jose import jwt

from app.core.environment import envs
from app.modules.auth.dtos.responses.auth.default_auth_response_dto import (
    DefaultAuthResponseDTO,
)
from app.modules.auth.exceptions.refresh_auth_error import RefreshAuthError
from app.modules.auth.services.user.user_service import UserService
from app.modules.auth.use_cases.auth.default_auth_use_case import DefaultAuthUseCase
from app.modules.user.exceptions.user_not_found_error import UserNotFoundError


class RefreshUserAuthUseCase:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    def handle(self, refresh_token: str) -> DefaultAuthResponseDTO:
        payload = self.__decode_refresh_token(refresh_token)
        if payload["type"] != "user-refresh":
            raise RefreshAuthError

        user = self.user_service.get_user_by_id(UUID(payload["sub"]))
        if user is None:
            raise UserNotFoundError

        return DefaultAuthUseCase.get_auth_response(user)

    @staticmethod
    def __decode_refresh_token(refresh_token: str) -> dict:
        try:
            return jwt.decode(refresh_token, envs.JWT_SECRET, algorithms=["HS256"])
        except Exception as e:
            raise RefreshAuthError from e
