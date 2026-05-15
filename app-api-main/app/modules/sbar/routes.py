from fastapi import APIRouter, Depends

from app.enums.models.permissions_enums import HospitalizationPermissionsEnum
from app.middlewares.auth_middleware import require_permission, verify_tenant_jwt
from app.modules.sbar.controllers.sbar_controller import extract_sbar
from app.modules.sbar.dtos.sbar_extract_dto import SbarExtractResponse

router = APIRouter(prefix="/api/sbar", tags=["sbar"])

router.add_api_route(
    path="/extract",
    endpoint=extract_sbar,
    methods=["POST"],
    response_model=SbarExtractResponse,
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(HospitalizationPermissionsEnum.READ.value)),
    ],
)
