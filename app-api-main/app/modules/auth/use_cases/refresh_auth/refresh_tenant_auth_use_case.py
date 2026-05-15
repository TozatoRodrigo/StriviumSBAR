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
from app.modules.auth.services.tenant.tenant_service import TenantService
from app.modules.auth.use_cases.auth.tenant_auth_use_case import TenantAuthUseCase
from app.modules.auth.utils.jwt import (
    REFRESH_TOKEN_EXPIRES_MINUTES,
    generate_refresh_token,
)


class RefreshTenantAuthUseCase:
    def __init__(
        self,
        tenant_service: TenantService,
        tenant_auth_use_case: TenantAuthUseCase,
        refresh_token_service: RefreshTokenService,
    ) -> None:
        self.tenant_service = tenant_service
        self.tenant_auth_use_case = tenant_auth_use_case
        self.refresh_token_service = refresh_token_service

    def handle(self, refresh_token: str) -> DefaultAuthResponseDTO:
        payload = self.__decode_refresh_token(refresh_token)
        if payload.get("type") != "tenant-refresh":
            raise RefreshAuthError

        try:
            tenant_id = UUID(payload["sub"])
            user_id = UUID(payload["user_id"])
        except (KeyError, TypeError, ValueError) as e:
            raise RefreshAuthError from e

        try:
            jti = UUID(jti_claim) if (jti_claim := payload.get("jti")) else None
        except (TypeError, ValueError) as e:
            raise RefreshAuthError from e

        new_jti, _token_family = self.refresh_token_service.validate_and_rotate(
            jti=jti,
            user_id=user_id,
            token_type="tenant-refresh",  # noqa: S106
            expires_minutes=REFRESH_TOKEN_EXPIRES_MINUTES,
        )

        self.tenant_service.get_tenant_by_id(tenant_id)
        access_token = self.tenant_auth_use_case.generate_access_token_from_ids(
            tenant_id, user_id
        )
        new_refresh = generate_refresh_token(
            {"sub": str(tenant_id), "type": "tenant-refresh", "user_id": str(user_id)},
            jti=new_jti,
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
