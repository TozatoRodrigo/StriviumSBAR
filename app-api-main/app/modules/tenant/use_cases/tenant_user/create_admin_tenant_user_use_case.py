from uuid import UUID

from app.enums.models.roles_names_enum import RolesNamesEnum
from app.modules.tenant.dtos.tenant_user.create_tenant_user import CreateTenantUserDTO
from app.modules.tenant.repositories.role_repository import RoleRepository
from app.modules.tenant.use_cases.tenant_user.create_tenant_user_use_case import (
    CreateTenantUserUseCase,
)


class CreateAdminTenantUserUseCase:
    def __init__(
        self,
        create_tenant_user_use_case: CreateTenantUserUseCase,
        role_repository: RoleRepository,
    ) -> None:
        self.create_tenant_user_use_case = create_tenant_user_use_case
        self.role_repository = role_repository

    def handle(self, tenant_id: UUID, user_id: UUID) -> None:
        role = self.role_repository.get_by_name(RolesNamesEnum.ADMIN.value)
        tenant_user_data = CreateTenantUserDTO(
            tenant_id=tenant_id,
            user_id=user_id,
            role_id=role.id,
        )
        self.create_tenant_user_use_case.handle(tenant_user_data)
