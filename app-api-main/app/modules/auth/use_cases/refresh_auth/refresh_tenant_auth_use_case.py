from uuid import UUID

from jose import jwt

from app.core.environment import envs
from app.modules.auth.dtos.responses.auth.default_auth_response_dto import (
    DefaultAuthResponseDTO,
)
from app.modules.auth.exceptions.refresh_auth_error import RefreshAuthError
from app.modules.auth.services.tenant.tenant_service import TenantService
from app.modules.auth.use_cases.auth.tenant_auth_use_case import TenantAuthUseCase


class RefreshTenantAuthUseCase:
    def __init__(
        self, tenant_service: TenantService, tenant_auth_use_case: TenantAuthUseCase
    ) -> None:
        self.tenant_service = tenant_service
        self.tenant_auth_use_case = tenant_auth_use_case

    def handle(self, refresh_token: str) -> DefaultAuthResponseDTO:
        payload = self.__decode_refresh_token(refresh_token)
        if payload["type"] != "tenant-refresh":
            raise RefreshAuthError

        return self.tenant_auth_use_case.handle(
            UUID(payload["sub"]), UUID(payload["user_id"])
        )

    @staticmethod
    def __decode_refresh_token(refresh_token: str) -> dict:
        try:
            return jwt.decode(refresh_token, envs.JWT_SECRET, algorithms=["HS256"])
        except Exception as e:
            raise RefreshAuthError from e
