from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.concerns.base_model import BaseModel
from app.models.medical_team import MedicalTeamStatus
from app.modules.medical_team.dtos.responses.medical_team.medical_team_user_response import (
    MedicalTeamUserResponse,
)


class DetailedMedicalTeamResponse(BaseModel):
    id: UUID = Field(description="ID do time médico")
    name: str = Field(description="Nome do time médico")
    description: str = Field(description="Descrição do time médico")
    status: MedicalTeamStatus = Field(description="Status do time médico")
    created_at: datetime = Field(description="Data de criação do time médico")
    updated_at: datetime = Field(description="Data de atualização do time médico")

    medical_team_users: list[MedicalTeamUserResponse] = Field(
        description="Usuários do time médico"
    )
