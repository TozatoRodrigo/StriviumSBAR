"""Purge audit logs older than the configured retention window (LGPD).

Run periodically (e.g. a daily cron job):

    poetry run python -m app.scripts.purge_audit_logs

Entries older than ``AUDIT_LOG_RETENTION_DAYS`` (default 180 ~ 6 months) are
deleted. The retention window must stay >= the legal minimum for traceability.
"""

from datetime import datetime, timedelta

from sqlmodel import Session

from app.core.database import engine
from app.core.environment import envs
from app.core.logging import logger
from app.modules.audit.repositories.audit_log_repository import AuditLogRepository


def purge_audit_logs() -> int:
    """Delete audit logs older than the retention window.

    Returns:
        The number of audit log rows removed.

    """
    cutoff = datetime.now() - timedelta(days=envs.AUDIT_LOG_RETENTION_DAYS)
    with Session(engine) as session:
        deleted = AuditLogRepository(session).delete_older_than(cutoff)

    logger.info(
        "Purged audit logs older than retention window",
        extra={
            "deleted": deleted,
            "retention_days": envs.AUDIT_LOG_RETENTION_DAYS,
            "cutoff": cutoff.isoformat(),
        },
    )
    return deleted


if __name__ == "__main__":
    purge_audit_logs()
