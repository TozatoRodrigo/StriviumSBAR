from fastapi import APIRouter, status

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
)
