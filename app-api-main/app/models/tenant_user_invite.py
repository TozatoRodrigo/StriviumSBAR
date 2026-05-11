from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from app.enums.models.tenant_user_invite_member_type_enums import (
    TenantUserInviteMemberType,
)
from app.enums.models.tenant_user_invite_status_enum import TenantUserInviteStatusEnum

if TYPE_CHECKING:
    from app.models.role import Role
    from app.models.tenant import Tenant


class TenantUserInvite(SQLModel, table=True):
    __tablename__ = "tenant_user_invites"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(nullable=False, foreign_key="tenants.id")
    role_id: UUID = Field(nullable=False, foreign_key="roles.id")
    email: str = Field(nullable=False, index=True)
    status: TenantUserInviteStatusEnum = Field(
        nullable=False, default=TenantUserInviteStatusEnum.PENDING
    )
    member_type: TenantUserInviteMemberType = Field(
        nullable=False, default=TenantUserInviteMemberType.DOCTOR
    )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    tenant: "Tenant" = Relationship(back_populates="tenant_user_invites")
    role: "Role" = Relationship(back_populates="tenant_user_invites")
