from datetime import datetime
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel


class PaginateAuditLogsDTO(BaseModel):
    page: int = Query(1, ge=1)
    limit: int = Query(10, ge=1, le=100)
    user_id: UUID | None = Query(None)
    action: str | None = Query(None)
    resource_type: str | None = Query(None)
    start_date: datetime | None = Query(None)
    end_date: datetime | None = Query(None)
