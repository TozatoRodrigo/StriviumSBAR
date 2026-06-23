from datetime import datetime
from typing import Any
from uuid import UUID

from app.concerns.base_model import BaseModel


class AuditLogResponseDTO(BaseModel):
    id: UUID
    user_id: UUID | None
    tenant_id: UUID | None
    action: str
    resource_type: str | None
    resource_id: str | None
    method: str | None
    path: str | None
    status_code: int | None
    ip_address: str | None
    user_agent: str | None
    changes: dict[str, Any] | None
    created_at: datetime
