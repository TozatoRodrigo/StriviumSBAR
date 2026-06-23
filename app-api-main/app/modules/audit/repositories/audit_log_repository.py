from datetime import datetime
from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, col, delete, select

from app.models.audit_log import AuditLog


class AuditLogRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, audit_log: AuditLog) -> AuditLog:
        self.session.add(audit_log)
        self.session.commit()
        self.session.refresh(audit_log)
        return audit_log

    def paginate(
        self,
        page: int,
        limit: int,
        *,
        user_id: UUID | None = None,
        action: str | None = None,
        resource_type: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> Page[AuditLog]:
        query = select(AuditLog).order_by(col(AuditLog.created_at).desc())

        if user_id is not None:
            query = query.where(AuditLog.user_id == user_id)
        if action is not None:
            query = query.where(AuditLog.action == action)
        if resource_type is not None:
            query = query.where(AuditLog.resource_type == resource_type)
        if start_date is not None:
            query = query.where(AuditLog.created_at >= start_date)
        if end_date is not None:
            query = query.where(AuditLog.created_at <= end_date)

        return paginate(self.session, query, Params(page=page, size=limit))

    def delete_older_than(self, cutoff: datetime) -> int:
        """Delete entries created before ``cutoff``.

        Returns:
            The number of rows removed.

        """
        result = self.session.exec(
            delete(AuditLog).where(col(AuditLog.created_at) < cutoff)
        )
        self.session.commit()
        return result.rowcount or 0
