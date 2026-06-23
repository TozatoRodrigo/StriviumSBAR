from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class AuditLog(SQLModel, table=True):
    """Immutable audit trail entry for sensitive actions (LGPD Art. 46/48).

    Records who did what, when and from where. ``changes`` optionally holds a
    ``{"before": ..., "after": ...}`` payload when a mutation use case provides
    it. To respect data minimization, the middleware records access metadata
    (action, resource, ip) rather than dumping full request bodies.
    """

    __tablename__: str = "audit_logs"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID | None = Field(default=None, nullable=True, index=True)
    tenant_id: UUID | None = Field(default=None, nullable=True, index=True)
    action: str = Field(nullable=False, index=True)
    resource_type: str | None = Field(default=None, nullable=True, index=True)
    resource_id: str | None = Field(default=None, nullable=True)
    method: str | None = Field(default=None, nullable=True)
    path: str | None = Field(default=None, nullable=True)
    status_code: int | None = Field(default=None, nullable=True)
    ip_address: str | None = Field(default=None, nullable=True)
    user_agent: str | None = Field(default=None, nullable=True)
    changes: dict[str, Any] | None = Field(
        default=None, sa_column=Column(JSON, nullable=True)
    )
    created_at: datetime = Field(default_factory=datetime.now, index=True)
