from uuid import UUID

from app.modules.medical_team.repositories.medical_team_repository import (
    MedicalTeamRepository,
)


class DeleteMedicalTeamUseCase:
    def __init__(self, medical_team_repository: MedicalTeamRepository) -> None:
        self.medical_team_repository = medical_team_repository

    def handle(self, medical_team_id: UUID) -> None:
        self.medical_team_repository.delete(medical_team_id)
