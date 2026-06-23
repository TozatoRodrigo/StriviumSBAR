from app.modules.audit.dtos.paginate_audit_logs_dto import PaginateAuditLogsDTO
from app.modules.audit.dtos.responses.paginate_audit_logs_response_dto import (
    PaginateAuditLogsResponseDTO,
)
from app.modules.audit.mappers.audit_log_mapper import AuditLogMapper
from app.modules.audit.repositories.audit_log_repository import AuditLogRepository


class PaginateAuditLogsUseCase:
    def __init__(self, audit_log_repository: AuditLogRepository) -> None:
        self.audit_log_repository = audit_log_repository

    def handle(self, params: PaginateAuditLogsDTO) -> PaginateAuditLogsResponseDTO:
        pagination = self.audit_log_repository.paginate(
            params.page,
            params.limit,
            user_id=params.user_id,
            action=params.action,
            resource_type=params.resource_type,
            start_date=params.start_date,
            end_date=params.end_date,
        )
        return AuditLogMapper.to_paginate_response(pagination)
