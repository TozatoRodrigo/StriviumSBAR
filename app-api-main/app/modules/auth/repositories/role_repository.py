from uuid import UUID

from sqlmodel import Session, select

from app.models.role import Role
from app.models.tenant_user import TenantUser


class RoleRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_role_by_user_id_and_tenant_id(
        self, user_id: UUID, tenant_id: UUID
    ) -> Role | None:
        return self.db.exec(
            select(Role)
            .join(TenantUser)
            .where(TenantUser.user_id == user_id, TenantUser.tenant_id == tenant_id)
        ).first()
