from uuid import UUID

from pydantic import BaseModel, Field


class CreateTenantUserDTO(BaseModel):
    tenant_id: UUID = Field(description="ID do tenant")
    user_id: UUID = Field(description="ID do usuário")
    role_id: UUID = Field(description="ID do papel")
