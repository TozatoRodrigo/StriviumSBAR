from fastapi import APIRouter, Depends

from app.middlewares.auth_middleware import verify_tenant_jwt, verify_user_jwt
from app.modules.tenant.dtos.responses.list_tenants_response_dto import (
    ListTenantsResponseDTO,
)
from app.modules.tenant.dtos.responses.tenant_response_dto import TenantResponseDTO

from .controllers.tenant_controller import (
    create_tenant,
    get_tenant,
    list_tenants_available,
)

router = APIRouter(prefix="/tenant/v1", tags=["tenant"])


router.add_api_route(
    path="/tenants",
    endpoint=create_tenant,
    methods=["POST"],
    response_model=TenantResponseDTO,
    dependencies=[Depends(verify_user_jwt)],
)

router.add_api_route(
    path="/tenants/available-for-user",
    endpoint=list_tenants_available,
    methods=["GET"],
    response_model=ListTenantsResponseDTO,
    dependencies=[Depends(verify_user_jwt)],
)

router.add_api_route(
    path="/tenants/{tenant_id}",
    endpoint=get_tenant,
    methods=["GET"],
    response_model=TenantResponseDTO,
    dependencies=[Depends(verify_tenant_jwt)],
)
