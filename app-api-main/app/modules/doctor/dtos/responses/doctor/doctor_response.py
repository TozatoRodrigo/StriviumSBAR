from uuid import UUID

from pydantic import Field

from app.concerns.base_model import BaseModel
from app.modules.doctor.dtos.responses.doctor.doctor_crm_response import (
    DoctorCrmResponseDTO,
)


class DoctorResponseDTO(BaseModel):
    id: UUID = Field(description="ID do médico")
    first_name: str = Field(description="Primeiro nome do médico")
    last_name: str = Field(description="Sobrenome do médico")
    crm: DoctorCrmResponseDTO = Field(description="Dados de CRM do médico")
