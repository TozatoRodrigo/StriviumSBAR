from uuid import UUID

from pydantic import Field

from app.concerns.base_model import BaseModel


class RoleResponse(BaseModel):
    id: UUID = Field(description="ID do papel")
    name: str = Field(description="Nome do papel")
    description: str = Field(description="Descrição do papel")
