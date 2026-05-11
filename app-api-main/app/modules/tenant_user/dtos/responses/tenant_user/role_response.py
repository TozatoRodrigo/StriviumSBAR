from uuid import UUID

from pydantic import BaseModel, Field


class RoleResponse(BaseModel):
    id: UUID = Field(description="ID do papel")
    name: str = Field(description="Nome do papel")
    description: str = Field(description="Descrição do papel")
