from fastapi_pagination import Page

from app.models.tenant_user import TenantUser
from app.modules.tenant_user.dtos.responses.tenant_user.detailed_tenant_user_response import (
    DetailedTenantUserResponse,
)
from app.modules.tenant_user.dtos.responses.tenant_user.paginate_tenant_users_response import (
    PaginateTenantUsersResponse,
)
from app.modules.tenant_user.dtos.responses.tenant_user.role_response import (
    RoleResponse,
)
from app.modules.tenant_user.dtos.responses.tenant_user.user_response import (
    UserResponse,
)


class TenantUserMapper:
    @staticmethod
    def to_detailed_response(tenant_user: TenantUser) -> DetailedTenantUserResponse:
        return DetailedTenantUserResponse(
            id=tenant_user.id,
            tenant_id=tenant_user.tenant_id,
            user_id=tenant_user.user_id,
            user=UserResponse(
                id=tenant_user.user.id,
                first_name=tenant_user.user.first_name,
                last_name=tenant_user.user.last_name,
                email=tenant_user.user.email,
            ),
            role_id=tenant_user.role_id,
            role=RoleResponse(
                id=tenant_user.role.id,
                name=tenant_user.role.name,
                description=tenant_user.role.description,
            ),
            member_type=tenant_user.member_type,
            created_at=tenant_user.created_at,
            updated_at=tenant_user.updated_at,
        )

    @staticmethod
    def to_paginate_response(
        pagination: Page[TenantUser],
    ) -> PaginateTenantUsersResponse:
        items = [
            TenantUserMapper.to_detailed_response(tenant_user)
            for tenant_user in pagination.items
        ]
        return PaginateTenantUsersResponse(
            data=items,
            total=pagination.total,
            page=pagination.page,
            limit=pagination.size,
            total_pages=pagination.pages,
        )
