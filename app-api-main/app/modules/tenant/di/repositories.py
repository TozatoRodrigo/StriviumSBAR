from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.modules.tenant.repositories.role_repository import RoleRepository
from app.modules.tenant.repositories.tenant_repository import TenantRepository
from app.modules.tenant.repositories.tenant_user_repository import TenantUserRepository


def get_tenant_repository(
    session: Annotated[Session, Depends(get_session)],
) -> TenantRepository:
    return TenantRepository(session)


def get_tenant_user_repository(
    session: Annotated[Session, Depends(get_session)],
) -> TenantUserRepository:
    return TenantUserRepository(session)


def get_role_repository(
    session: Annotated[Session, Depends(get_session)],
) -> RoleRepository:
    return RoleRepository(session)
