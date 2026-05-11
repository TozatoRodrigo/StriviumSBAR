from uuid import UUID

from pydantic import Field

from app.concerns.base_model import BaseModel


class TenantAuthRequestDTO(BaseModel):
    tenant_id: UUID = Field(description="ID do tenant")
