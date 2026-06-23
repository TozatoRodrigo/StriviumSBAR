from fastapi import APIRouter, Depends, status

from app.enums.models.audit_enums import AuditLogPermissionsEnum
from app.middlewares.auth_middleware import require_permission, verify_tenant_jwt
from app.modules.audit.controllers.audit_log_controller import paginate_audit_logs
from app.modules.audit.dtos.responses.paginate_audit_logs_response_dto import (
    PaginateAuditLogsResponseDTO,
)

router = APIRouter(
    prefix="/audit/v1",
    tags=["audit"],
)

router.add_api_route(
    path="/logs",
    endpoint=paginate_audit_logs,
    response_model=PaginateAuditLogsResponseDTO,
    methods=["GET"],
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(AuditLogPermissionsEnum.READ.value)),
    ],
    status_code=status.HTTP_200_OK,
)
