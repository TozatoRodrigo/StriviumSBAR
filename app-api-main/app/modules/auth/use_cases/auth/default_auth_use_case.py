from app.models.user import User
from app.modules.auth.dtos.requests.auth.default_auth_request_dto import (
    DefaultAuthRequestDTO,
)
from app.modules.auth.dtos.responses.auth.default_auth_response_dto import (
    DefaultAuthResponseDTO,
)
from app.modules.auth.exceptions.auth_error import AuthError
from app.modules.auth.services.user.user_service import UserService
from app.modules.auth.utils.bcrypt import verify_hash
from app.modules.auth.utils.jwt import (
    ACCESS_TOKEN_EXPIRES_MINUTES,
    ACCESS_TOKEN_TYPE,
    generate_access_token,
    generate_refresh_token,
)


class DefaultAuthUseCase:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    def handle(self, data: DefaultAuthRequestDTO) -> DefaultAuthResponseDTO:
        user = self.user_service.get_user_by_login(data.login)
        if not user:
            raise AuthError
        if not verify_hash(data.password, user.password):
            raise AuthError

        return self.get_auth_response(user)

    @staticmethod
    def get_auth_response(user: User) -> DefaultAuthResponseDTO:
        access_token = DefaultAuthUseCase.get_access_token(user)
        refresh_token = DefaultAuthUseCase.get_refresh_token(user)
        return DefaultAuthResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=ACCESS_TOKEN_TYPE,
            expires_in=ACCESS_TOKEN_EXPIRES_MINUTES,
        )

    @staticmethod
    def get_access_token(user: User) -> str:
        payload = {
            "sub": str(user.id),
            "type": "user",
            "user": {
                "id": str(user.id),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
        }
        return generate_access_token(payload)

    @staticmethod
    def get_refresh_token(user: User) -> str:
        payload = {
            "sub": str(user.id),
            "type": "user-refresh",
        }
        return generate_refresh_token(payload)
