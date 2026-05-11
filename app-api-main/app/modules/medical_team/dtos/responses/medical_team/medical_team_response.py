from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.concerns.base_model import BaseModel
from app.models.medical_team import MedicalTeamStatus


class MedicalTeamResponse(BaseModel):
    id: UUID = Field(
        description="ID do time médico",
    )
    name: str = Field(
        description="Nome do time médico",
        examples=["Time Médico 1"],
    )
    description: str = Field(
        description="Descrição do time médico",
        examples=["Descrição do time médico 1"],
    )
    status: MedicalTeamStatus = Field(
        description="Status do time médico",
    )
    created_at: datetime = Field(
        description="Data de criação do time médico",
    )
    updated_at: datetime = Field(
        description="Data de atualização do time médico",
    )
