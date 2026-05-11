from uuid import UUID

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: UUID = Field(description="ID do usuário")
    first_name: str = Field(description="Nome do usuário")
    last_name: str = Field(description="Sobrenome do usuário")
    email: str = Field(description="Email do usuário")
