from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.core.database import get_session
from app.modules.audit.repositories.audit_log_repository import AuditLogRepository


def get_audit_log_repository(
    session: Annotated[Session, Depends(get_session)],
) -> AuditLogRepository:
    return AuditLogRepository(session)
