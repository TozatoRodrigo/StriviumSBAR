from uuid import UUID

from pydantic import Field

from app.concerns.base_model import BaseModel


class PaginateHospitalizationsDTO(BaseModel):
    page: int = Field(default=1, ge=1, description="Página", examples=[1])
    limit: int = Field(default=10, ge=1, description="Limite", examples=[10])
    patient_id: UUID | None = Field(
        default=None, description="ID do paciente", examples=[None]
    )
    search: str | None = Field(default=None, description="Busca", examples=["John Doe"])
