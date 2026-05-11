from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.hospitalization import Hospitalization
    from app.models.tenant_user_invite import TenantUserInvite


class Tenant(SQLModel, table=True):
    __tablename__: str = "tenants"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False)
    logo_url: str | None = Field(nullable=True, default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    hospitalizations: list["Hospitalization"] = Relationship(back_populates="tenant")
    tenant_user_invites: list["TenantUserInvite"] = Relationship(
        back_populates="tenant"
    )
