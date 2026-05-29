from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    jti: UUID = Field(default_factory=uuid4, unique=True, nullable=False)
    user_id: UUID = Field(nullable=False, index=True)
    token_family: UUID = Field(default_factory=uuid4, nullable=False, index=True)
    token_type: str = Field(nullable=False)
    expires_at: datetime = Field(nullable=False)
    revoked_at: datetime | None = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.now)
