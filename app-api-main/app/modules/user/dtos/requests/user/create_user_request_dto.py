from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateUserRequestDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str = Field(
        min_length=3,
        max_length=150,
        description="Primeiro nome do usuário",
        examples=["Jhon"],
    )
    last_name: str = Field(
        min_length=3,
        max_length=150,
        description="Sobrenome do usuário",
        examples=["Doe"],
    )
    crm_state: str | None = Field(
        max_length=2,
        description="Estado do CRM do médico",
        examples=["SP"],
        default=None,
    )
    crm_number: str | None = Field(
        max_length=50,
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
    password: str = Field(
        min_length=6,
        description="Senha do usuário (mínimo 6 caracteres)",
        examples=["MinhaSenhaForte123@"],
    )
    birth_date: date = Field(description="Data de nascimento do usuário")
