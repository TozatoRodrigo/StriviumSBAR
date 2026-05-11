from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.concerns.base_model import BaseModel
from app.enums.models.medical_team_users_enums import MedicalTeamUserStatus


class MedicalTeamUserResponse(BaseModel):
    id: UUID = Field(description="ID do usuário")
    first_name: str = Field(description="Nome do usuário")
    last_name: str = Field(description="Sobrenome do usuário")
    email: str = Field(description="Email do usuário")
    status: MedicalTeamUserStatus = Field(description="Status do usuário")
    created_at: datetime = Field(description="Data de criação do usuário")
    updated_at: datetime = Field(description="Data de atualização do usuário")
