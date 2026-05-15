from fastapi import APIRouter, Depends, status

from app.enums.models.permissions_enums import MedicalTeamPermissionsEnum
from app.middlewares.auth_middleware import require_permission, verify_tenant_jwt
from app.modules.medical_team.dtos.responses.medical_team.detailed_medical_team_response import (
    DetailedMedicalTeamResponse,
)
from app.modules.medical_team.dtos.responses.medical_team.medical_team_response import (
    MedicalTeamResponse,
)
from app.modules.medical_team.dtos.responses.medical_team.paginate_medical_teams_response import (
    PaginateMedicalTeamsResponse,
)

from .controllers.medical_team_controller import (
    create_medical_team,
    delete_medical_team,
    get_medical_team_by_id,
    paginate_medical_team,
    update_medical_team,
)

router = APIRouter(prefix="/medical-team/v1", tags=["medical-team"])

router.add_api_route(
    path="/medical-teams",
    endpoint=paginate_medical_team,
    methods=["GET"],
    response_model=PaginateMedicalTeamsResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(MedicalTeamPermissionsEnum.READ.value)),
    ],
)

router.add_api_route(
    path="/medical-teams",
    endpoint=create_medical_team,
    response_model=MedicalTeamResponse,
    status_code=status.HTTP_201_CREATED,
    methods=["POST"],
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(MedicalTeamPermissionsEnum.CREATE.value)),
    ],
)

router.add_api_route(
    path="/medical-teams/{medical_team_id}",
    endpoint=update_medical_team,
    response_model=MedicalTeamResponse,
    status_code=status.HTTP_200_OK,
    methods=["PUT"],
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(MedicalTeamPermissionsEnum.UPDATE.value)),
    ],
)

router.add_api_route(
    path="/medical-teams/{medical_team_id}",
    endpoint=delete_medical_team,
    methods=["DELETE"],
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(MedicalTeamPermissionsEnum.DELETE.value)),
    ],
)

router.add_api_route(
    path="/medical-teams/{medical_team_id}",
    endpoint=get_medical_team_by_id,
    methods=["GET"],
    response_model=DetailedMedicalTeamResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(MedicalTeamPermissionsEnum.READ.value)),
    ],
)
