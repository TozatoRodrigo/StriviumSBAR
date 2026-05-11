from uuid import UUID

from fastapi_pagination import Page

from app.models.medical_team import MedicalTeam
from app.modules.medical_team.dtos.medical_team.create_medical_team_dto import (
    CreateMedicalTeamDTO,
)
from app.modules.medical_team.dtos.responses.medical_team.detailed_medical_team_response import (
    DetailedMedicalTeamResponse,
)
from app.modules.medical_team.dtos.responses.medical_team.medical_team_response import (
    MedicalTeamResponse,
)
from app.modules.medical_team.dtos.responses.medical_team.medical_team_user_response import (
    MedicalTeamUserResponse,
)
from app.modules.medical_team.dtos.responses.medical_team.paginate_medical_teams_response import (
    PaginateMedicalTeamsResponse,
)


class MedicalTeamMapper:
    def __init__(self, tenant_id: UUID) -> None:
        self.tenant_id = tenant_id

    def to_entity(self, medical_team_dto: CreateMedicalTeamDTO) -> MedicalTeam:
        return MedicalTeam(
            tenant_id=self.tenant_id,
            name=medical_team_dto.name,
            description=medical_team_dto.description,
        )

    @staticmethod
    def to_detailed_response(medical_team: MedicalTeam) -> DetailedMedicalTeamResponse:
        medical_team_users = [
            MedicalTeamUserResponse(
                id=medical_team_user.id,
                first_name=medical_team_user.user.first_name,
                last_name=medical_team_user.user.last_name,
                email=medical_team_user.user.email,
                status=medical_team_user.status,
                created_at=medical_team_user.created_at,
                updated_at=medical_team_user.updated_at,
            )
            for medical_team_user in medical_team.medical_team_users
        ]
        return DetailedMedicalTeamResponse(
            id=medical_team.id,
            name=medical_team.name,
            description=medical_team.description,
            status=medical_team.status,
            created_at=medical_team.created_at,
            updated_at=medical_team.updated_at,
            medical_team_users=medical_team_users,
        )

    @staticmethod
    def to_response(medical_team: MedicalTeam) -> MedicalTeamResponse:
        return MedicalTeamResponse(
            id=medical_team.id,
            name=medical_team.name,
            description=medical_team.description,
            status=medical_team.status,
            created_at=medical_team.created_at,
            updated_at=medical_team.updated_at,
        )

    @staticmethod
    def to_paginate_response(data: Page[MedicalTeam]) -> PaginateMedicalTeamsResponse:
        items = [MedicalTeamMapper.to_response(item) for item in data.items]
        return PaginateMedicalTeamsResponse(
            data=items,
            page=data.page,
            limit=data.size,
            total=data.total,
        )
