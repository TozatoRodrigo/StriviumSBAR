from pydantic import BaseModel, Field


class RoleResponse(BaseModel):
    name: str = Field(description="Nome do papel")
    description: str = Field(description="Descrição do papel")
