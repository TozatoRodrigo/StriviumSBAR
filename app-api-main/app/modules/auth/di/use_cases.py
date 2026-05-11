from typing import Annotated

from fastapi import Depends

from app.modules.auth.di.repositories import (
    get_permission_repository,
    get_role_repository,
)
from app.modules.auth.di.services import get_tenant_service, get_user_service
from app.modules.auth.repositories.permission_repository import PermissionRepository
from app.modules.auth.repositories.role_repository import RoleRepository
from app.modules.auth.services.tenant.tenant_service import TenantService
from app.modules.auth.services.user.user_service import UserService
from app.modules.auth.use_cases.auth.default_auth_use_case import DefaultAuthUseCase
from app.modules.auth.use_cases.auth.tenant_auth_use_case import TenantAuthUseCase
from app.modules.auth.use_cases.refresh_auth.refresh_tenant_auth_use_case import (
    RefreshTenantAuthUseCase,
)
from app.modules.auth.use_cases.refresh_auth.refresh_user_auth_use_case import (
    RefreshUserAuthUseCase,
)


def get_default_auth_use_case(
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> DefaultAuthUseCase:
    return DefaultAuthUseCase(user_service)


def get_tenant_auth_use_case(
    tenant_service: Annotated[TenantService, Depends(get_tenant_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
    permission_repository: Annotated[
        PermissionRepository, Depends(get_permission_repository)
    ],
) -> TenantAuthUseCase:
    return TenantAuthUseCase(
        tenant_service, user_service, role_repository, permission_repository
    )


def get_refresh_user_auth_use_case(
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> RefreshUserAuthUseCase:
    return RefreshUserAuthUseCase(user_service)


def get_refresh_tenant_auth_use_case(
    tenant_service: Annotated[TenantService, Depends(get_tenant_service)],
    tenant_auth_use_case: Annotated[
        TenantAuthUseCase, Depends(get_tenant_auth_use_case)
    ],
) -> RefreshTenantAuthUseCase:
    return RefreshTenantAuthUseCase(tenant_service, tenant_auth_use_case)
