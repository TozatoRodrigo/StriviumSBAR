from uuid import UUID

from app.exceptions.tenant_not_found import TenantNotFoundError
from app.models.tenant import Tenant
from app.modules.tenant.repositories.tenant_repository import TenantRepository


class TenantService:
    def __init__(self, tenant_repository: TenantRepository) -> None:
        self.tenant_repository = tenant_repository

    def get_tenant_by_id(self, tenant_id: UUID) -> Tenant:
        tenant = self.tenant_repository.get_tenant_by_id(tenant_id)
        if tenant is None:
            raise TenantNotFoundError

        return tenant
