from app.modules.tenant.mappers.tenant_mapper import TenantMapper
from app.modules.tenant.mappers.tenant_user_mapper import TenantUserMapper


def get_tenant_mapper() -> TenantMapper:
    return TenantMapper()


def get_tenant_user_mapper() -> TenantUserMapper:
    return TenantUserMapper()
