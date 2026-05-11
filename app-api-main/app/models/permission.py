from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Permission(SQLModel, table=True):
    __tablename__ = "permissions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    code: str = Field(nullable=False, unique=True)
    name: str = Field(nullable=False, unique=True)
    description: str | None = Field(nullable=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
