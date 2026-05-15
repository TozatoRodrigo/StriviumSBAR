from uuid import UUID

from app.exceptions.tenant_not_found import TenantNotFoundError
from app.modules.tenant.dtos.requests.update_tenant_request_dto import (
    UpdateTenantRequestDTO,
)
from app.modules.tenant.dtos.responses.tenant_response_dto import TenantResponseDTO
from app.modules.tenant.mappers.tenant_mapper import TenantMapper
from app.modules.tenant.repositories.tenant_repository import TenantRepository


class UpdateTenantUseCase:
    def __init__(
        self, tenant_repository: TenantRepository, tenant_mapper: TenantMapper
    ) -> None:
        self.tenant_repository = tenant_repository
        self.tenant_mapper = tenant_mapper

    def handle(
        self, tenant_id: UUID, data: UpdateTenantRequestDTO
    ) -> TenantResponseDTO:
        tenant = self.tenant_repository.get_tenant_by_id(tenant_id)
        if tenant is None:
            raise TenantNotFoundError

        tenant.name = data.name
        tenant = self.tenant_repository.save(tenant)
        return self.tenant_mapper.to_response(tenant)
