from uuid import UUID

from app.exceptions.medical_team_not_found_error import MedicalTeamNotFoundError
from app.modules.medical_team.dtos.medical_team.update_medical_team_dto import (
    UpdateMedicalTeamDTO,
)
from app.modules.medical_team.dtos.responses.medical_team.medical_team_response import (
    MedicalTeamResponse,
)
from app.modules.medical_team.mappers.medical_team_mapper import MedicalTeamMapper
from app.modules.medical_team.repositories.medical_team_repository import (
    MedicalTeamRepository,
)


class UpdateMedicalTeamUseCase:
    def __init__(
        self,
        medical_team_repository: MedicalTeamRepository,
        medical_team_mapper: MedicalTeamMapper,
    ) -> None:
        self.medical_team_repository = medical_team_repository
        self.medical_team_mapper = medical_team_mapper

    def handle(
        self, medical_team_id: UUID, medical_team_data: UpdateMedicalTeamDTO
    ) -> MedicalTeamResponse:
        medical_team = self.medical_team_repository.get_by_id(medical_team_id)
        if not medical_team:
            raise MedicalTeamNotFoundError
        medical_team.name = medical_team_data.name or medical_team.name
        medical_team.description = (
            medical_team_data.description or medical_team.description
        )
        medical_team = self.medical_team_repository.save(medical_team)
        return self.medical_team_mapper.to_response(medical_team)
