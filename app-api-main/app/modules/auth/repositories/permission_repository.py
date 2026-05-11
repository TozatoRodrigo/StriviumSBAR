from uuid import UUID

from sqlmodel import Session, select

from app.models.permission import Permission
from app.models.role_permission import RolePermission


class PermissionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_permissions_by_role_id(self, role_id: UUID) -> list[Permission]:
        permissions = self.db.exec(
            select(Permission)
            .join(RolePermission)
            .where(RolePermission.role_id == role_id)
        )
        return list(permissions)
