from datetime import date

from pydantic import BaseModel, EmailStr, Field


class UpdateDoctorDTO(BaseModel):
    full_name: str = Field(
        description="Nome completo do médico",
        min_length=5,
        examples=["João da Silva"],
    )
    birth_date: date = Field(description="Data de nascimento do médico")
    cellphone: str = Field(description="Telefone do médico", examples=["41999999999"])
    gender: str = Field(description="Gênero do médico", examples=["male"])
    document: str = Field(
        description="CPF do médico (apenas números)",
        examples=["12345678910"],
    )
    email: EmailStr = Field(description="E-mail do médico")
    specialty: str = Field(
        description="Especialidade do médico", examples=["CARDIOLOGY"]
    )
    crm_uf: str = Field(description="UF do CRM do médico", min_length=2, max_length=2)
    crm_number: str = Field(description="Número do CRM do médico", max_length=50)
