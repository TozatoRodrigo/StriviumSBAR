from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from app.enums.models.tenant_user_member_type_enums import TenantUserMemberType

if TYPE_CHECKING:
    from app.models.role import Role
    from app.models.user import User


class TenantUser(SQLModel, table=True):
    __tablename__: str = "tenant_users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(nullable=False, foreign_key="tenants.id")
    user_id: UUID = Field(nullable=False, foreign_key="users.id")
    role_id: UUID = Field(nullable=False, foreign_key="roles.id")
    member_type: TenantUserMemberType = Field(
        nullable=False, default=TenantUserMemberType.DOCTOR
    )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    user: "User" = Relationship(back_populates="tenant_users")
    role: "Role" = Relationship(back_populates="tenant_users")
