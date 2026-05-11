from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict, Field

from app.concerns.base_model import BaseModel


class TenantResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(description="ID do tenant")
    name: str = Field(description="Nome do tenant", examples=["Santa casa"])
    logo_url: str | None = Field(
        description="URL da logo do tenant",
        default=None,
        examples=["https://storage.googleapis.com/santacasa-storage/logo.png"],
    )
    created_at: datetime = Field(description="Data de criação do tenant")
    updated_at: datetime = Field(description="Data de atualização do tenant")
