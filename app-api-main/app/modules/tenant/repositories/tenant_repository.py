from uuid import UUID

from sqlmodel import Session, select

from app.models.tenant import Tenant
from app.models.tenant_user import TenantUser


class TenantRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, tenant: Tenant) -> Tenant:
        self.session.add(tenant)
        self.session.commit()
        self.session.refresh(tenant)
        return tenant

    def get_tenant_by_id(self, tenant_id: UUID) -> Tenant | None:
        return self.session.exec(select(Tenant).where(Tenant.id == tenant_id)).first()

    def list_tenants_available_for_user(self, user_id: UUID) -> list[Tenant]:
        query = (
            select(Tenant)
            .join(TenantUser, Tenant.id == TenantUser.tenant_id)
            .where(TenantUser.user_id == user_id)
            .distinct()
        )
        return self.session.exec(query).all()
