from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.core.database import get_session
from app.modules.tenant_user.repositories.role_repository import RoleRepository


def get_role_repository(
    session: Annotated[Session, Depends(get_session)],
) -> RoleRepository:
    return RoleRepository(session)
