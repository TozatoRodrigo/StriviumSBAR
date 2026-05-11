from typing import Annotated

from fastapi import Depends

from app.modules.auth.services.tenant.tenant_service import TenantService
from app.modules.auth.services.user.user_service import UserService
from app.modules.tenant.di.repositories import get_tenant_repository
from app.modules.tenant.repositories.tenant_repository import TenantRepository
from app.modules.user.di.repositories import get_user_repository
from app.modules.user.interfaces.repositories.user_repository import UserRepository


def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(user_repository)


def get_tenant_service(
    tenant_repository: Annotated[TenantRepository, Depends(get_tenant_repository)],
) -> TenantService:
    return TenantService(tenant_repository)
