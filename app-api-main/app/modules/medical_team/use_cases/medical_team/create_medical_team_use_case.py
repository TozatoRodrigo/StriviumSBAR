from app.models.medical_team import MedicalTeam
from app.modules.medical_team.dtos.responses.medical_team.medical_team_response import (
    MedicalTeamResponse,
)
from app.modules.medical_team.mappers.medical_team_mapper import MedicalTeamMapper
from app.modules.medical_team.repositories.medical_team_repository import (
    MedicalTeamRepository,
)


class CreateMedicalTeamUseCase:
    def __init__(
        self,
        medical_team_repository: MedicalTeamRepository,
        medical_team_mapper: MedicalTeamMapper,
    ) -> None:
        self.medical_team_repository = medical_team_repository
        self.medical_team_mapper = medical_team_mapper

    def handle(self, medical_team: MedicalTeam) -> MedicalTeamResponse:
        medical_team_entity = self.medical_team_mapper.to_entity(medical_team)
        medical_team = self.medical_team_repository.save(medical_team_entity)
        return self.medical_team_mapper.to_response(medical_team)
