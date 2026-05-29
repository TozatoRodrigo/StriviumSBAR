from app.models.user import User
from app.modules.auth.dtos.requests.auth.default_auth_request_dto import (
    DefaultAuthRequestDTO,
)
from app.modules.auth.dtos.responses.auth.default_auth_response_dto import (
    DefaultAuthResponseDTO,
)
from app.modules.auth.exceptions.auth_error import AuthError
from app.modules.auth.services.refresh_token.refresh_token_service import (
    RefreshTokenService,
)
from app.modules.auth.services.user.user_service import UserService
from app.modules.auth.utils.bcrypt import verify_hash
from app.modules.auth.utils.jwt import (
    ACCESS_TOKEN_EXPIRES_MINUTES,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_EXPIRES_MINUTES,
    generate_access_token,
    generate_refresh_token,
)


class DefaultAuthUseCase:
    def __init__(
        self, user_service: UserService, refresh_token_service: RefreshTokenService
    ) -> None:
        self.user_service = user_service
        self.refresh_token_service = refresh_token_service

    def handle(self, data: DefaultAuthRequestDTO) -> DefaultAuthResponseDTO:
        user = self.user_service.get_user_by_login(data.login)
        if not user:
            raise AuthError
        if not verify_hash(data.password, user.password):
            raise AuthError

        return self.get_auth_response(user)

    def get_auth_response(self, user: User) -> DefaultAuthResponseDTO:
        access_token = self.get_access_token(user)
        refresh_token = self.get_refresh_token(user)
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

    def get_refresh_token(self, user: User) -> str:
        jti, _token_family = self.refresh_token_service.create_token_record(
            user_id=user.id,
            token_type="user-refresh",  # noqa: S106
            expires_minutes=REFRESH_TOKEN_EXPIRES_MINUTES,
        )
        payload = {
            "sub": str(user.id),
            "type": "user-refresh",
        }
        return generate_refresh_token(payload, jti=jti)
