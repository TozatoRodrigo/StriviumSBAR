from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.enums.models.tenant_user_member_type_enums import TenantUserMemberType
from app.modules.tenant_user.dtos.responses.tenant_user.role_response import (
    RoleResponse,
)
from app.modules.tenant_user.dtos.responses.tenant_user.user_response import (
    UserResponse,
)


class DetailedTenantUserResponse(BaseModel):
    id: UUID = Field(description="ID do vínculo de tenant e usuário")
    tenant_id: UUID = Field(description="ID do tenant")
    user_id: UUID = Field(description="ID do usuário")
    user: UserResponse = Field(description="Dados do usuário")
    role_id: UUID = Field(description="ID do papel")
    role: RoleResponse = Field(description="Dados do papel")
    member_type: TenantUserMemberType = Field(description="Tipo de membro")
    created_at: datetime = Field(description="Data de criação do usuário")
    updated_at: datetime = Field(description="Data de atualização do usuário")
