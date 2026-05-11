from uuid import UUID

from app.exceptions.user_not_found_error import UserNotFoundError
from app.models.permission import Permission
from app.models.role import Role
from app.models.tenant import Tenant
from app.models.user import User
from app.modules.auth.dtos.responses.auth.tenant_auth_response_dto import (
    TenantAuthResponseDTO,
)
from app.modules.auth.repositories.permission_repository import PermissionRepository
from app.modules.auth.repositories.role_repository import RoleRepository
from app.modules.auth.services.tenant.tenant_service import TenantService
from app.modules.auth.services.user.user_service import UserService
from app.modules.auth.utils.jwt import (
    ACCESS_TOKEN_EXPIRES_MINUTES,
    ACCESS_TOKEN_TYPE,
    generate_access_token,
    generate_refresh_token,
)


class TenantAuthUseCase:
    def __init__(
        self,
        tenant_service: TenantService,
        user_service: UserService,
        role_repository: RoleRepository,
        permission_repository: PermissionRepository,
    ) -> None:
        self.tenant_service = tenant_service
        self.user_service = user_service
        self.role_repository = role_repository
        self.permission_repository = permission_repository

    def handle(self, tenant_id: UUID, user_id: UUID) -> TenantAuthResponseDTO:
        tenant = self.tenant_service.get_tenant_by_id(tenant_id)
        user = self.get_user(user_id)
        user_role = self.get_user_role(user_id, tenant_id)
        permissions = self.permission_repository.get_permissions_by_role_id(
            user_role.id
        )
        access_token = self.generate_access_token(tenant, user, user_role, permissions)
        refresh_token = self.generate_refresh_token(tenant, user_id)
        return TenantAuthResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=ACCESS_TOKEN_TYPE,
            expires_in=ACCESS_TOKEN_EXPIRES_MINUTES,
        )

    def get_user(self, user_id: UUID) -> User:
        user = self.user_service.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError
        return user

    def get_user_role(self, user_id: UUID, tenant_id: UUID) -> Role:
        user_role = self.role_repository.get_role_by_user_id_and_tenant_id(
            user_id, tenant_id
        )
        if user_role is None:
            raise UserNotFoundError
        return user_role

    @staticmethod
    def generate_access_token(
        tenant: Tenant, user: User, user_role: Role, permissions: list[Permission]
    ) -> str:
        payload = {
            "sub": str(tenant.id),
            "type": "tenant",
            "tenant": {
                "id": str(tenant.id),
                "name": tenant.name,
            },
            "user": {
                "id": str(user.id),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
            "role": {
                "id": str(user_role.id),
                "name": user_role.name,
                "permissions": [
                    {
                        "code": permission.code,
                        "name": permission.name,
                    }
                    for permission in permissions
                ],
            },
        }
        return generate_access_token(payload)

    @staticmethod
    def generate_refresh_token(tenant: Tenant, user_id: UUID) -> str:
        payload = {
            "sub": str(tenant.id),
            "type": "tenant-refresh",
            "user_id": str(user_id),
        }
        return generate_refresh_token(payload)
