from fastapi import APIRouter, status

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
)

router.add_api_route(
    path="/medical-teams",
    endpoint=create_medical_team,
    response_model=MedicalTeamResponse,
    status_code=status.HTTP_201_CREATED,
    methods=["POST"],
)

router.add_api_route(
    path="/medical-teams/{medical_team_id}",
    endpoint=update_medical_team,
    response_model=MedicalTeamResponse,
    status_code=status.HTTP_200_OK,
    methods=["PUT"],
)

router.add_api_route(
    path="/medical-teams/{medical_team_id}",
    endpoint=delete_medical_team,
    methods=["DELETE"],
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)

router.add_api_route(
    path="/medical-teams/{medical_team_id}",
    endpoint=get_medical_team_by_id,
    methods=["GET"],
    response_model=DetailedMedicalTeamResponse,
    status_code=status.HTTP_200_OK,
)
