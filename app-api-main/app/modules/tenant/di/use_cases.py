from typing import Annotated

from fastapi import Depends

from app.di.services import get_logged_user_service
from app.modules.tenant.di.mappers import get_tenant_mapper, get_tenant_user_mapper
from app.modules.tenant.di.repositories import (
    get_role_repository,
    get_tenant_repository,
    get_tenant_user_repository,
)
from app.modules.tenant.mappers.tenant_mapper import TenantMapper
from app.modules.tenant.mappers.tenant_user_mapper import TenantUserMapper
from app.modules.tenant.repositories.role_repository import RoleRepository
from app.modules.tenant.repositories.tenant_repository import TenantRepository
from app.modules.tenant.repositories.tenant_user_repository import TenantUserRepository
from app.modules.tenant.use_cases.tenant.create_tenant_use_case import (
    CreateTenantUseCase,
)
from app.modules.tenant.use_cases.tenant.get_tenant_data_use_case import (
    GetTenantDataUseCase,
)
from app.modules.tenant.use_cases.tenant.list_tenants_available_for_user_use_case import (
    ListTenantsAvailableForUserUseCase,
)
from app.modules.tenant.use_cases.tenant.update_tenant_use_case import (
    UpdateTenantUseCase,
)
from app.modules.tenant.use_cases.tenant_user.create_admin_tenant_user_use_case import (
    CreateAdminTenantUserUseCase,
)
from app.modules.tenant.use_cases.tenant_user.create_tenant_user_use_case import (
    CreateTenantUserUseCase,
)
from app.services.logged_user.logged_user_service import LoggedUserService


def get_create_tenant_user_use_case(
    tenant_user_repository: Annotated[
        TenantUserRepository, Depends(get_tenant_user_repository)
    ],
    tenant_user_mapper: Annotated[TenantUserMapper, Depends(get_tenant_user_mapper)],
) -> CreateTenantUserUseCase:
    return CreateTenantUserUseCase(tenant_user_repository, tenant_user_mapper)


def get_create_admin_tenant_user_use_case(
    create_tenant_user_use_case: Annotated[
        CreateTenantUserUseCase, Depends(get_create_tenant_user_use_case)
    ],
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
) -> CreateAdminTenantUserUseCase:
    return CreateAdminTenantUserUseCase(create_tenant_user_use_case, role_repository)


def get_create_tenant_use_case(
    tenant_repository: Annotated[TenantRepository, Depends(get_tenant_repository)],
    tenant_mapper: Annotated[TenantMapper, Depends(get_tenant_mapper)],
    logged_user_service: Annotated[LoggedUserService, Depends(get_logged_user_service)],
    create_admin_tenant_user_use_case: Annotated[
        CreateAdminTenantUserUseCase, Depends(get_create_admin_tenant_user_use_case)
    ],
) -> CreateTenantUseCase:
    return CreateTenantUseCase(
        tenant_repository,
        tenant_mapper,
        logged_user_service,
        create_admin_tenant_user_use_case,
    )


def get_list_tenants_available_for_user_use_case(
    tenant_repository: Annotated[TenantRepository, Depends(get_tenant_repository)],
    tenant_mapper: Annotated[TenantMapper, Depends(get_tenant_mapper)],
    logged_user_service: Annotated[LoggedUserService, Depends(get_logged_user_service)],
) -> ListTenantsAvailableForUserUseCase:
    return ListTenantsAvailableForUserUseCase(
        tenant_repository,
        tenant_mapper,
    )


def get_get_tenant_data_use_case(
    tenant_repository: Annotated[TenantRepository, Depends(get_tenant_repository)],
    tenant_mapper: Annotated[TenantMapper, Depends(get_tenant_mapper)],
) -> GetTenantDataUseCase:
    return GetTenantDataUseCase(tenant_repository, tenant_mapper)


def get_update_tenant_use_case(
    tenant_repository: Annotated[TenantRepository, Depends(get_tenant_repository)],
    tenant_mapper: Annotated[TenantMapper, Depends(get_tenant_mapper)],
) -> UpdateTenantUseCase:
    return UpdateTenantUseCase(tenant_repository, tenant_mapper)
