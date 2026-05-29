from pydantic import Field

from app.concerns.base_model import BaseModel


class DoctorCrmResponseDTO(BaseModel):
    uf: str = Field(description="UF do CRM")
    number: str = Field(description="Número do CRM")
