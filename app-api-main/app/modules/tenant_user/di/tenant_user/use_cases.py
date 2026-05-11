from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.modules.tenant_user.di.tenant_user.mappers import get_tenant_user_mapper
from app.modules.tenant_user.di.tenant_user.repositories import (
    get_tenant_user_repository,
)
from app.modules.tenant_user.mappers.tenant_user_mapper import TenantUserMapper
from app.modules.tenant_user.repositories.tenant_user_repository import (
    TenantUserRepository,
)
from app.modules.tenant_user.use_cases.tenant_user.paginate_tenant_users_use_case import (
    PaginateTenantUsersUseCase,
)
from app.services.tenant.tenant_service import get_tenant_id_from_token


def get_paginate_tenant_users_use_case(
    tenant_user_repository: Annotated[
        TenantUserRepository, Depends(get_tenant_user_repository)
    ],
    tenant_user_mapper: Annotated[TenantUserMapper, Depends(get_tenant_user_mapper)],
    tenant_id: Annotated[UUID, Depends(get_tenant_id_from_token)],
) -> PaginateTenantUsersUseCase:
    return PaginateTenantUsersUseCase(
        tenant_user_repository, tenant_user_mapper, tenant_id
    )
