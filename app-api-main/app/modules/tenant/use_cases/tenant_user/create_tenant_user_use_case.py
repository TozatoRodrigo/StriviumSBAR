from app.models.tenant_user import TenantUser
from app.modules.tenant.dtos.tenant_user.create_tenant_user import CreateTenantUserDTO
from app.modules.tenant.mappers.tenant_user_mapper import TenantUserMapper
from app.modules.tenant.repositories.tenant_user_repository import TenantUserRepository


class CreateTenantUserUseCase:
    def __init__(
        self,
        tenant_user_repository: TenantUserRepository,
        tenant_user_mapper: TenantUserMapper,
    ) -> None:
        self.tenant_user_repository = tenant_user_repository
        self.tenant_user_mapper = tenant_user_mapper

    def handle(self, tenant_user_data: CreateTenantUserDTO) -> TenantUser:
        tenant_user_entity = self.tenant_user_mapper.to_entity(tenant_user_data)
        return self.tenant_user_repository.save(tenant_user_entity)
