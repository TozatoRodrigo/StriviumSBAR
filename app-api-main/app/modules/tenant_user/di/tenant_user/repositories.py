from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.core.database import get_session
from app.modules.tenant_user.repositories.tenant_user_repository import (
    TenantUserRepository,
)


def get_tenant_user_repository(
    session: Annotated[Session, Depends(get_session)],
) -> TenantUserRepository:
    return TenantUserRepository(session)
