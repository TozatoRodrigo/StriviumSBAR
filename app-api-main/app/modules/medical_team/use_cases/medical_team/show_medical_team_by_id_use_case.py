from uuid import UUID

from app.exceptions.medical_team_not_found_error import MedicalTeamNotFoundError
from app.modules.medical_team.dtos.responses.medical_team.detailed_medical_team_response import (
    DetailedMedicalTeamResponse,
)
from app.modules.medical_team.mappers.medical_team_mapper import MedicalTeamMapper
from app.modules.medical_team.repositories.medical_team_repository import (
    MedicalTeamRepository,
)


class ShowMedicalTeamByIdUseCase:
    def __init__(
        self,
        medical_team_repository: MedicalTeamRepository,
        medical_team_mapper: MedicalTeamMapper,
        tenant_id: UUID,
    ) -> None:
        self.medical_team_repository = medical_team_repository
        self.medical_team_mapper = medical_team_mapper
        self.tenant_id = tenant_id

    def handle(self, medical_team_id: UUID) -> DetailedMedicalTeamResponse:
        medical_team = self.medical_team_repository.show_by_id_and_tenant_id(
            medical_team_id, self.tenant_id
        )
        if not medical_team:
            raise MedicalTeamNotFoundError
        return self.medical_team_mapper.to_detailed_response(medical_team)
