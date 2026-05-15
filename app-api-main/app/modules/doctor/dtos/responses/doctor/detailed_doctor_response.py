from datetime import date, datetime
from uuid import UUID

from pydantic import EmailStr, Field

from app.concerns.base_model import BaseModel


class DetailedDoctorResponseDTO(BaseModel):
    id: UUID = Field(description="ID do médico")
    full_name: str = Field(description="Nome completo do médico")
    birth_date: date = Field(description="Data de nascimento do médico")
    cellphone: str = Field(description="Celular do médico")
    gender: str = Field(description="Gênero do médico")
    document: str = Field(description="CPF do médico")
    email: EmailStr = Field(description="Email do médico")
    specialty: str = Field(description="Especialidade do médico")
    crm_uf: str = Field(description="UF do CRM")
    crm_number: str = Field(description="Número do CRM")
    created_at: datetime = Field(description="Data de criação")
    updated_at: datetime = Field(description="Data de atualização")
