from datetime import date, datetime
from uuid import UUID

from pydantic import Field

from app.concerns.base_model import BaseModel


class PatientResponseDTO(BaseModel):
    id: UUID = Field(description="ID do paciente")
    first_name: str = Field(description="Nome do paciente", examples=["João"])
    last_name: str = Field(description="Sobrenome do paciente", examples=["Silva"])
    document_number: str | None = Field(
        description="Número do documento do paciente", examples=["06511313085"]
    )
    birth_date: date = Field(description="Data de nascimento do paciente")
    created_at: datetime = Field(description="Data de criação do paciente")
    updated_at: datetime = Field(description="Data de atualização do paciente")
