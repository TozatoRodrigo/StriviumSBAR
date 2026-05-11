from uuid import UUID

from pydantic import BaseModel, Field


class TenantResponse(BaseModel):
    id: UUID = Field(description="ID do tenant")
    name: str = Field(description="Nome do tenant")
    logo_url: str | None = Field(description="URL da logo do tenant")
