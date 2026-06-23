from typing import Annotated

from fastapi import Depends

from app.modules.audit.di.repositories import get_audit_log_repository
from app.modules.audit.repositories.audit_log_repository import AuditLogRepository
from app.modules.audit.use_cases.paginate_audit_logs_use_case import (
    PaginateAuditLogsUseCase,
)


def get_paginate_audit_logs_use_case(
    audit_log_repository: Annotated[
        AuditLogRepository, Depends(get_audit_log_repository)
    ],
) -> PaginateAuditLogsUseCase:
    return PaginateAuditLogsUseCase(audit_log_repository)
