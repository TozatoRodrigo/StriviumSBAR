from uuid import UUID

from pydantic import Field

from app.concerns.base_model import BaseModel


class PatientResponse(BaseModel):
    id: UUID = Field(description="ID do paciente")
    first_name: str = Field(description="Nome do paciente")
    last_name: str = Field(description="Sobrenome do paciente")
