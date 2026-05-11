from sqlalchemy.orm import Session

from app.models.tenant_user import TenantUser


class TenantUserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, tenant_user: TenantUser) -> TenantUser:
        self.session.add(tenant_user)
        self.session.commit()
        self.session.refresh(tenant_user)
        return tenant_user
