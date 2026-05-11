from uuid import UUID

from sqlalchemy.orm import joinedload
from sqlmodel import Session, func, select

from app.enums.models.tenant_user_invite_status_enum import TenantUserInviteStatusEnum
from app.models.tenant_user_invite import TenantUserInvite


class TenantUserInviteRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, tenant_user_invite: TenantUserInvite) -> None:
        self.session.add(tenant_user_invite)
        self.session.commit()
        return tenant_user_invite

    def list_pendings_by_email(self, email: str) -> list[TenantUserInvite]:
        query = (
            select(TenantUserInvite)
            .where(
                TenantUserInvite.email == email,
                TenantUserInvite.status == TenantUserInviteStatusEnum.PENDING,
            )
            .options(
                joinedload(TenantUserInvite.tenant), joinedload(TenantUserInvite.role)
            )
        )
        return self.session.exec(query).all()

    def get_by_id(self, invite_id: UUID) -> TenantUserInvite | None:
        return self.session.exec(
            select(TenantUserInvite).where(TenantUserInvite.id == invite_id)
        ).first()

    def get_pending_invites_count_by_email(self, email: str) -> int:
        query = select(func.count(TenantUserInvite.id)).where(
            TenantUserInvite.email == email,
            TenantUserInvite.status == TenantUserInviteStatusEnum.PENDING,
        )
        return self.session.exec(query).one()

    def list_pendings_by_tenant_id(self, tenant_id: UUID) -> list[TenantUserInvite]:
        query = (
            select(TenantUserInvite)
            .where(
                TenantUserInvite.tenant_id == tenant_id,
                TenantUserInvite.status == TenantUserInviteStatusEnum.PENDING,
            )
            .options(
                joinedload(TenantUserInvite.role), joinedload(TenantUserInvite.tenant)
            )
        )
        return self.session.exec(query).all()
