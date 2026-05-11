from app.modules.tenant_user.mappers.tenant_user_mapper import TenantUserMapper


def get_tenant_user_mapper() -> TenantUserMapper:
    return TenantUserMapper()
