from uuid import UUID

from app.modules.tenant.dtos.responses.list_tenants_response_dto import (
    ListTenantsResponseDTO,
)
from app.modules.tenant.mappers.tenant_mapper import TenantMapper
from app.modules.tenant.repositories.tenant_repository import TenantRepository


class ListTenantsAvailableForUserUseCase:
    def __init__(
        self,
        tenant_repository: TenantRepository,
        tenant_mapper: TenantMapper,
    ) -> None:
        self.tenant_repository = tenant_repository
        self.tenant_mapper = tenant_mapper

    def handle(self, user_id: UUID) -> ListTenantsResponseDTO:
        tenants = self.tenant_repository.list_tenants_available_for_user(user_id)
        return self.tenant_mapper.to_response_list(tenants)
