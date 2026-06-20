from fastapi import APIRouter, Depends

from app.dtos.exception.exception_dto import ExceptionDTO
from app.middlewares.turnstile_middleware import verify_turnstile_token
from app.modules.auth.controllers.auth_controller import login, tenant_auth
from app.modules.auth.controllers.refresh_auth_controller import (
    refresh_tenant_auth,
    refresh_user_auth,
)
from app.modules.auth.dtos.responses.auth.default_auth_response_dto import (
    DefaultAuthResponseDTO,
)
from app.modules.auth.dtos.responses.auth.tenant_auth_response_dto import (
    TenantAuthResponseDTO,
)

router = APIRouter(prefix="/auth/v1", tags=["auth"])

router.add_api_route(
    "/login",
    login,
    methods=["POST"],
    dependencies=[Depends(verify_turnstile_token)],
    responses={
        200: {"model": DefaultAuthResponseDTO},
        401: {"model": ExceptionDTO},
    },
)

router.add_api_route(
    "/tenant",
    tenant_auth,
    methods=["POST"],
    response_model=TenantAuthResponseDTO,
)

router.add_api_route(
    "/refresh/user",
    refresh_user_auth,
    methods=["POST"],
    response_model=DefaultAuthResponseDTO,
)

router.add_api_route(
    "/refresh/tenant",
    refresh_tenant_auth,
    methods=["POST"],
    response_model=TenantAuthResponseDTO,
)
