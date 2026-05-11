from typing import Annotated

from fastapi import Body, Depends, status
from fastapi.responses import JSONResponse

from app.modules.auth.di.use_cases import (
    get_refresh_tenant_auth_use_case,
    get_refresh_user_auth_use_case,
)
from app.modules.auth.use_cases.refresh_auth.refresh_tenant_auth_use_case import (
    RefreshTenantAuthUseCase,
)
from app.modules.auth.use_cases.refresh_auth.refresh_user_auth_use_case import (
    RefreshUserAuthUseCase,
)


def refresh_user_auth(
    refresh_token: Annotated[str, Body(embed=True)],
    refresh_user_auth_use_case: Annotated[
        RefreshUserAuthUseCase, Depends(get_refresh_user_auth_use_case)
    ],
) -> JSONResponse:
    auth_data = refresh_user_auth_use_case.handle(refresh_token)
    return JSONResponse(auth_data.to_json(), status_code=status.HTTP_200_OK)


def refresh_tenant_auth(
    refresh_token: Annotated[str, Body(embed=True)],
    refresh_tenant_auth_use_case: Annotated[
        RefreshTenantAuthUseCase, Depends(get_refresh_tenant_auth_use_case)
    ],
) -> JSONResponse:
    auth_data = refresh_tenant_auth_use_case.handle(refresh_token)
    return JSONResponse(auth_data.to_json(), status_code=status.HTTP_200_OK)
