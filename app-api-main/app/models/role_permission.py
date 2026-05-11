from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class RolePermission(SQLModel, table=True):
    __tablename__ = "role_permissions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    role_id: UUID = Field(nullable=False, foreign_key="roles.id")
    permission_id: UUID = Field(nullable=False, foreign_key="permissions.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
