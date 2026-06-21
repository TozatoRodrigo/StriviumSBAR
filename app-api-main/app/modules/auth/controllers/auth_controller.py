from typing import Annotated
from uuid import UUID

from fastapi import Depends, Request, status
from fastapi.responses import JSONResponse

from app.core.rate_limiter import AUTH_LOGIN_LIMIT, AUTH_TENANT_LIMIT, limiter
from app.di.services import get_user_id_from_token
from app.modules.auth.di.use_cases import (
    get_default_auth_use_case,
    get_tenant_auth_use_case,
)
from app.modules.auth.dtos.requests.auth.default_auth_request_dto import (
    DefaultAuthRequestDTO,
)
from app.modules.auth.dtos.requests.auth.tenant_auth_request_dto import (
    TenantAuthRequestDTO,
)
from app.modules.auth.use_cases.auth.default_auth_use_case import DefaultAuthUseCase
from app.modules.auth.use_cases.auth.tenant_auth_use_case import TenantAuthUseCase


@limiter.limit(AUTH_LOGIN_LIMIT)
def login(
    request: Request,
    data: DefaultAuthRequestDTO,
    default_auth_use_case: Annotated[
        DefaultAuthUseCase, Depends(get_default_auth_use_case)
    ],
) -> JSONResponse:
    auth_data = default_auth_use_case.handle(data)
    return JSONResponse(auth_data.to_json(), status_code=status.HTTP_200_OK)


@limiter.limit(AUTH_TENANT_LIMIT)
def tenant_auth(
    request: Request,
    request_data: TenantAuthRequestDTO,
    user_id: Annotated[UUID, Depends(get_user_id_from_token)],
    tenant_auth_use_case: Annotated[
        TenantAuthUseCase, Depends(get_tenant_auth_use_case)
    ],
) -> JSONResponse:
    auth_data = tenant_auth_use_case.handle(request_data.tenant_id, user_id)
    return JSONResponse(auth_data.to_json(), status_code=status.HTTP_200_OK)
