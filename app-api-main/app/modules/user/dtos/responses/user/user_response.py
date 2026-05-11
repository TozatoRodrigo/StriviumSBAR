from datetime import date
from uuid import UUID

from pydantic import ConfigDict, EmailStr, Field

from app.concerns.base_model import BaseModel


class UserResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(description="ID do usuário")
    first_name: str = Field(
        description="Primeiro nome do usuário",
        examples=["Jhon"],
    )
    last_name: str = Field(
        description="Sobrenome do usuário",
        examples=["Doe"],
    )
    crm_state: str | None = Field(
        description="Estado do CRM do médico",
        examples=["SP"],
        default=None,
    )
    crm_number: str | None = Field(
        description="Número do CRM do médico",
        examples=["123456"],
        default=None,
    )
    document: str | None = Field(
        pattern=r"^\d{11}$",
        description="CPF do usuário (apenas números)",
        default=None,
    )
    email: EmailStr = Field(description="Email do usuário")
    birth_date: date = Field(description="Data de nascimento do usuário")
