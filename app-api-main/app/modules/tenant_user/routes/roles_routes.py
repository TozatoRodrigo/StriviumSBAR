from fastapi import APIRouter, Depends, status

from app.enums.models.permissions_enums import TenantUserPermissionsEnum
from app.middlewares.auth_middleware import require_permission, verify_tenant_jwt
from app.modules.tenant_user.controllers.role_controller import list_roles
from app.modules.tenant_user.dtos.responses.role.list_roles_response import (
    ListRolesResponse,
)

router = APIRouter(prefix="/tenant-user/v1/roles", tags=["roles"])

router.add_api_route(
    "",
    endpoint=list_roles,
    methods=["GET"],
    status_code=status.HTTP_200_OK,
    response_model=ListRolesResponse,
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(TenantUserPermissionsEnum.READ.value)),
    ],
)
