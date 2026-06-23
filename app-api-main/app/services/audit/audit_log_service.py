import logging
from datetime import datetime
from typing import Any
from uuid import UUID

from sqlmodel import Session

from app.core.database import engine
from app.core.environment import envs
from app.models.audit_log import AuditLog
from app.modules.audit.repositories.audit_log_repository import AuditLogRepository

log = logging.getLogger("logger")


class AuditLogService:
    """Persist audit trail entries for sensitive actions (LGPD Art. 46/48)."""

    def __init__(self, repository: AuditLogRepository) -> None:
        self.repository = repository

    def record(
        self,
        *,
        action: str,
        user_id: UUID | None = None,
        tenant_id: UUID | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        method: str | None = None,
        path: str | None = None,
        status_code: int | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        changes: dict[str, Any] | None = None,
    ) -> AuditLog:
        entry = AuditLog(
            action=action,
            user_id=user_id,
            tenant_id=tenant_id,
            resource_type=resource_type,
            resource_id=resource_id,
            method=method,
            path=path,
            status_code=status_code,
            ip_address=ip_address,
            user_agent=user_agent,
            changes=changes,
            created_at=datetime.now(),
        )
        return self.repository.save(entry)


def record_audit_event(**kwargs: Any) -> None:
    """Record an audit event using a self-contained DB session.

    Safe to call from middleware: respects ``AUDIT_LOG_ENABLED`` and never
    raises, so auditing failures cannot break the request being audited.
    """
    if not envs.AUDIT_LOG_ENABLED:
        return

    try:
        with Session(engine) as session:
            AuditLogService(AuditLogRepository(session)).record(**kwargs)
    except Exception:
        log.exception("Failed to record audit log event")
