from app.models.tenant import Tenant
from app.modules.tenant.dtos.requests.create_tenant_request_dto import (
    CreateTenantRequestDTO,
)
from app.modules.tenant.dtos.responses.list_tenants_response_dto import (
    ListTenantsResponseDTO,
)
from app.modules.tenant.dtos.responses.tenant_response_dto import TenantResponseDTO


class TenantMapper:
    @staticmethod
    def to_entity(tenant_data: CreateTenantRequestDTO) -> Tenant:
        return Tenant(name=tenant_data.name)

    @staticmethod
    def to_response(tenant: Tenant) -> TenantResponseDTO:
        return TenantResponseDTO(
            id=tenant.id,
            name=tenant.name,
            logo_url=tenant.logo_url,  # TODO: add logo url
            created_at=tenant.created_at,
            updated_at=tenant.updated_at,
        )

    @staticmethod
    def to_response_list(tenants: list[Tenant]) -> ListTenantsResponseDTO:
        items = [TenantMapper.to_response(tenant) for tenant in tenants]
        return ListTenantsResponseDTO(data=items)
