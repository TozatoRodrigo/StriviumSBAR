from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.tenant_user import TenantUser
    from app.models.tenant_user_invite import TenantUserInvite


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False, unique=True)
    description: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    tenant_users: list["TenantUser"] = Relationship(back_populates="role")
    tenant_user_invites: list["TenantUserInvite"] = Relationship(back_populates="role")
