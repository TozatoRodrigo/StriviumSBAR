from pydantic import Field

from app.concerns.base_model import BaseModel
from app.modules.patients.dtos.responses.patient.patient_response_dto import (
    PatientResponseDTO,
)


class PaginatePatientsResponseDTO(BaseModel):
    data: list[PatientResponseDTO]
    total: int = Field(title="Número total de pacientes", examples=[30])
    page: int = Field(title="Número da página atual", examples=[1])
    limit: int = Field(title="Limite de pacientes por página", examples=[10])
    total_pages: int = Field(title="Número total de páginas", examples=[3])
