from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.core.database import get_session
from app.modules.auth.repositories.permission_repository import PermissionRepository
from app.modules.auth.repositories.role_repository import RoleRepository


def get_permission_repository(
    db: Annotated[Session, Depends(get_session)],
) -> PermissionRepository:
    return PermissionRepository(db)


def get_role_repository(db: Annotated[Session, Depends(get_session)]) -> RoleRepository:
    return RoleRepository(db)
