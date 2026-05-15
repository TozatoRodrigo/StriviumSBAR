from pydantic import Field

from app.concerns.base_model import BaseModel
from app.modules.doctor.dtos.responses.doctor.doctor_response import DoctorResponseDTO


class PaginateDoctorsResponseDTO(BaseModel):
    data: list[DoctorResponseDTO] = Field(description="Lista de médicos")
    total: int = Field(description="Total de médicos")
    page: int = Field(description="Página atual")
    limit: int = Field(description="Limite por página")
    total_pages: int = Field(description="Total de páginas")
