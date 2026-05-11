from app.models.tenant_user import TenantUser
from app.modules.tenant.dtos.tenant_user.create_tenant_user import CreateTenantUserDTO


class TenantUserMapper:
    @staticmethod
    def to_entity(tenant_user_data: CreateTenantUserDTO) -> TenantUser:
        return TenantUser(
            tenant_id=tenant_user_data.tenant_id,
            user_id=tenant_user_data.user_id,
            role_id=tenant_user_data.role_id,
        )
