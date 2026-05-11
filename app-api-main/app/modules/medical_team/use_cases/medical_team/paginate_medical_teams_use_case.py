from app.modules.medical_team.dtos.medical_team.paginate_medical_teams_dto import (
    PaginateMedicalTeamsDTO,
)
from app.modules.medical_team.dtos.responses.medical_team.paginate_medical_teams_response import (
    PaginateMedicalTeamsResponse,
)
from app.modules.medical_team.mappers.medical_team_mapper import MedicalTeamMapper
from app.modules.medical_team.repositories.medical_team_repository import (
    MedicalTeamRepository,
)


class PaginateMedicalTeamsUseCase:
    def __init__(
        self,
        medical_team_repository: MedicalTeamRepository,
        mapper: MedicalTeamMapper,
    ) -> None:
        self.medical_team_repository = medical_team_repository
        self.mapper = mapper

    def handle(self, params: PaginateMedicalTeamsDTO) -> PaginateMedicalTeamsResponse:
        data = self.medical_team_repository.paginate(
            params.page, params.limit, params.search
        )
        return self.mapper.to_paginate_response(data)
