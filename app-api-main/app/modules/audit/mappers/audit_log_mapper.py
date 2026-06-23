from fastapi_pagination import Page

from app.models.audit_log import AuditLog
from app.modules.audit.dtos.responses.audit_log_response_dto import AuditLogResponseDTO
from app.modules.audit.dtos.responses.paginate_audit_logs_response_dto import (
    PaginateAuditLogsResponseDTO,
)


class AuditLogMapper:
    @staticmethod
    def to_response(audit_log: AuditLog) -> AuditLogResponseDTO:
        return AuditLogResponseDTO(
            id=audit_log.id,
            user_id=audit_log.user_id,
            tenant_id=audit_log.tenant_id,
            action=audit_log.action,
            resource_type=audit_log.resource_type,
            resource_id=audit_log.resource_id,
            method=audit_log.method,
            path=audit_log.path,
            status_code=audit_log.status_code,
            ip_address=audit_log.ip_address,
            user_agent=audit_log.user_agent,
            changes=audit_log.changes,
            created_at=audit_log.created_at,
        )

    @staticmethod
    def to_paginate_response(
        pagination: Page[AuditLog],
    ) -> PaginateAuditLogsResponseDTO:
        return PaginateAuditLogsResponseDTO(
            data=[AuditLogMapper.to_response(item) for item in pagination.items],
            total=pagination.total,
            page=pagination.page,
            limit=pagination.size,
            total_pages=pagination.pages,
        )
