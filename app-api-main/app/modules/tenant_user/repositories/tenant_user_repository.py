from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlmodel import paginate
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from app.models.tenant_user import TenantUser


class TenantUserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, tenant_user: TenantUser) -> TenantUser:
        self.session.add(tenant_user)
        self.session.commit()
        self.session.refresh(tenant_user)
        return tenant_user

    def paginate(
        self, page: int, limit: int, search: str | None, tenant_id: UUID
    ) -> Page[TenantUser]:
        query = select(TenantUser).where(TenantUser.tenant_id == tenant_id)
        if search:
            query = query.join(TenantUser.user).where(
                TenantUser.user.first_name.ilike(f"%{search}%"),
                TenantUser.user.last_name.ilike(f"%{search}%"),
            )
        query = query.options(joinedload(TenantUser.user), joinedload(TenantUser.role))
        return paginate(self.session, query, Params(page=page, size=limit))
