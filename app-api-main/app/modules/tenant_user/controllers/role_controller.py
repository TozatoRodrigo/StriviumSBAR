from typing import Annotated

from fastapi import Depends, status
from fastapi.responses import JSONResponse

from app.modules.tenant_user.di.role.use_cases import get_list_roles_use_case
from app.modules.tenant_user.use_cases.role.list_roles_use_case import ListRolesUseCase


def list_roles(
    use_case: Annotated[ListRolesUseCase, Depends(get_list_roles_use_case)],
) -> JSONResponse:
    result = use_case.handle()
    return JSONResponse(content=result.to_json(), status_code=status.HTTP_200_OK)
