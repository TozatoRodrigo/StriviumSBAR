from typing import Annotated

from fastapi import Depends, Query, status
from fastapi.responses import JSONResponse

from app.modules.tenant_user.di.tenant_user.use_cases import (
    get_paginate_tenant_users_use_case,
)
from app.modules.tenant_user.dtos.tenant_user.paginate_tenant_users_params_dto import (
    PaginateTenantUsersParamsDTO,
)
from app.modules.tenant_user.use_cases.tenant_user.paginate_tenant_users_use_case import (
    PaginateTenantUsersUseCase,
)


def paginate_tenant_users(
    params: Annotated[PaginateTenantUsersParamsDTO, Query()],
    use_case: Annotated[
        PaginateTenantUsersUseCase, Depends(get_paginate_tenant_users_use_case)
    ],
) -> JSONResponse:
    result = use_case.handle(params)
    return JSONResponse(content=result.to_json(), status_code=status.HTTP_200_OK)
