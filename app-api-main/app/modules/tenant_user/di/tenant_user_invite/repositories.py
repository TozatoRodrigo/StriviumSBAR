from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.modules.tenant_user.repositories.tenant_user_invite_repository import (
    TenantUserInviteRepository,
)


def get_tenant_user_invite_repository(
    session: Annotated[Session, Depends(get_session)],
) -> TenantUserInviteRepository:
    return TenantUserInviteRepository(session)
