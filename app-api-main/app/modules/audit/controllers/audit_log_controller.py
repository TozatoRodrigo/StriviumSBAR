from typing import Annotated

from fastapi import Depends, Query, status
from fastapi.responses import JSONResponse

from app.modules.audit.di.use_cases import get_paginate_audit_logs_use_case
from app.modules.audit.dtos.paginate_audit_logs_dto import PaginateAuditLogsDTO
from app.modules.audit.use_cases.paginate_audit_logs_use_case import (
    PaginateAuditLogsUseCase,
)


def paginate_audit_logs(
    params: Annotated[PaginateAuditLogsDTO, Query()],
    paginate_audit_logs_use_case: Annotated[
        PaginateAuditLogsUseCase, Depends(get_paginate_audit_logs_use_case)
    ],
) -> JSONResponse:
    response = paginate_audit_logs_use_case.handle(params)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response.to_json(),
    )
