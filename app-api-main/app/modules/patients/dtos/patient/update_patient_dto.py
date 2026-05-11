from datetime import date

from pydantic import BaseModel, Field


class UpdatePatientDTO(BaseModel):
    first_name: str = Field(description="Nome do paciente", examples=["João"])
    last_name: str = Field(description="Sobrenome do paciente", examples=["Silva"])
    document_number: str | None = Field(
        default=None,
        description="Número do documento do paciente",
        examples=["06511313085"],
    )
    birth_date: date = Field(description="Data de nascimento do paciente")
