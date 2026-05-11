from typing import Annotated
from uuid import UUID

from fastapi import Depends, status
from fastapi.responses import JSONResponse

from app.di.services import get_user_id_from_token
from app.modules.tenant.di.use_cases import (
    get_create_tenant_use_case,
    get_get_tenant_data_use_case,
    get_list_tenants_available_for_user_use_case,
)
from app.modules.tenant.dtos.requests.create_tenant_request_dto import (
    CreateTenantRequestDTO,
)
from app.modules.tenant.use_cases.tenant.create_tenant_use_case import (
    CreateTenantUseCase,
)
from app.modules.tenant.use_cases.tenant.get_tenant_data_use_case import (
    GetTenantDataUseCase,
)
from app.modules.tenant.use_cases.tenant.list_tenants_available_for_user_use_case import (
    ListTenantsAvailableForUserUseCase,
)


def create_tenant(
    tenant_data: Annotated[CreateTenantRequestDTO, Depends()],
    create_tenant_use_case: Annotated[
        CreateTenantUseCase, Depends(get_create_tenant_use_case)
    ],
) -> JSONResponse:
    tenant_response = create_tenant_use_case.handle(tenant_data)
    return JSONResponse(
        content=tenant_response.to_json(), status_code=status.HTTP_201_CREATED
    )


def list_tenants_available(
    user_id: Annotated[UUID, Depends(get_user_id_from_token)],
    list_tenants_available_for_user_use_case: Annotated[
        ListTenantsAvailableForUserUseCase,
        Depends(get_list_tenants_available_for_user_use_case),
    ],
) -> JSONResponse:
    tenants_response = list_tenants_available_for_user_use_case.handle(user_id)
    return JSONResponse(
        content=tenants_response.to_json(), status_code=status.HTTP_200_OK
    )


def get_tenant(
    tenant_id: UUID,
    get_tenant_data_use_case: Annotated[
        GetTenantDataUseCase, Depends(get_get_tenant_data_use_case)
    ],
) -> JSONResponse:
    tenant_response = get_tenant_data_use_case.handle(tenant_id)
    return JSONResponse(
        content=tenant_response.to_json(), status_code=status.HTTP_200_OK
    )
