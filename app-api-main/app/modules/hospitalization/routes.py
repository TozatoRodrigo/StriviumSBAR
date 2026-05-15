from fastapi import APIRouter, Depends

from app.enums.models.permissions_enums import HospitalizationPermissionsEnum
from app.middlewares.auth_middleware import require_permission, verify_tenant_jwt
from app.modules.hospitalization.controllers.hospitalization_action_controller import (
    create_hospitalization_action,
    get_hospitalization_action,
    paginate_hospitalization_actions,
    update_hospitalization_action,
)
from app.modules.hospitalization.controllers.hospitalization_controller import (
    create_hospitalization,
    get_hospitalization,
    paginate_completed_hospitalizations,
    paginate_hospitalizations,
    paginate_pendings_hospitalizations,
    update_hospitalization,
)
from app.modules.hospitalization.dtos.responses.hospitalization.hospitalization_response import (
    HospitalizationResponse,
)
from app.modules.hospitalization.dtos.responses.hospitalization.paginate_hospitalization_response import (
    PaginateHospitalizationResponse,
)
from app.modules.hospitalization.dtos.responses.hospitalization_action.hospitalization_action_response import (
    HospitalizationActionResponse,
)
from app.modules.hospitalization.dtos.responses.hospitalization_action.paginate_hospitalization_action_response import (
    PaginateHospitalizationActionResponse,
)

router = APIRouter(
    prefix="/hospitalization/v1",
    tags=["hospitalizations"],
)

router.add_api_route(
    path="/hospitalizations",
    endpoint=create_hospitalization,
    response_model=HospitalizationResponse,
    methods=["POST"],
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(HospitalizationPermissionsEnum.CREATE.value)),
    ],
)

router.add_api_route(
    path="/hospitalizations",
    endpoint=paginate_hospitalizations,
    response_model=PaginateHospitalizationResponse,
    methods=["GET"],
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(HospitalizationPermissionsEnum.READ.value)),
    ],
)

router.add_api_route(
    path="/hospitalizations/pendings",
    endpoint=paginate_pendings_hospitalizations,
    response_model=PaginateHospitalizationResponse,
    methods=["GET"],
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(HospitalizationPermissionsEnum.READ.value)),
    ],
)

router.add_api_route(
    path="/hospitalizations/completed",
    endpoint=paginate_completed_hospitalizations,
    response_model=PaginateHospitalizationResponse,
    methods=["GET"],
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(HospitalizationPermissionsEnum.READ.value)),
    ],
)

router.add_api_route(
    path="/hospitalizations/{hospitalization_id}",
    endpoint=get_hospitalization,
    response_model=HospitalizationResponse,
    methods=["GET"],
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(HospitalizationPermissionsEnum.READ.value)),
    ],
)

router.add_api_route(
    path="/hospitalizations/{hospitalization_id}",
    endpoint=update_hospitalization,
    response_model=HospitalizationResponse,
    methods=["PUT"],
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(HospitalizationPermissionsEnum.UPDATE.value)),
    ],
)

# Hospitalization actions
hospitalization_action_router = APIRouter(
    prefix="/hospitalization/v1/hospitalizations/{hospitalization_id}/hospitalization-actions",
    tags=["hospitalization-actions"],
)

hospitalization_action_router.add_api_route(
    path="",
    endpoint=create_hospitalization_action,
    methods=["POST"],
    response_model=HospitalizationActionResponse,
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(HospitalizationPermissionsEnum.UPDATE.value)),
    ],
)

hospitalization_action_router.add_api_route(
    path="/{hospitalization_action_id}",
    endpoint=update_hospitalization_action,
    methods=["PUT"],
    response_model=HospitalizationActionResponse,
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(HospitalizationPermissionsEnum.UPDATE.value)),
    ],
)


hospitalization_action_router.add_api_route(
    path="",
    endpoint=paginate_hospitalization_actions,
    methods=["GET"],
    response_model=PaginateHospitalizationActionResponse,
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(HospitalizationPermissionsEnum.READ.value)),
    ],
)

hospitalization_action_router.add_api_route(
    path="/{hospitalization_action_id}",
    endpoint=get_hospitalization_action,
    methods=["GET"],
    response_model=HospitalizationActionResponse,
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(HospitalizationPermissionsEnum.READ.value)),
    ],
)
