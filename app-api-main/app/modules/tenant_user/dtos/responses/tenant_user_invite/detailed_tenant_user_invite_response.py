from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.concerns.base_model import BaseModel
from app.enums.models.tenant_user_invite_member_type_enums import (
    TenantUserInviteMemberType,
)
from app.enums.models.tenant_user_invite_status_enum import TenantUserInviteStatusEnum
from app.modules.tenant_user.dtos.responses.tenant_user_invite.role_response import (
    RoleResponse,
)
from app.modules.tenant_user.dtos.responses.tenant_user_invite.tenant_response import (
    TenantResponse,
)


class DetailedTenantUserInviteResponse(BaseModel):
    id: UUID = Field(description="ID do convite")
    tenant_id: UUID = Field(description="ID do tenant")
    tenant: TenantResponse = Field(description="Tenant do convite")
    role: RoleResponse = Field(description="Role do convite")
    email: str = Field(description="Email do convite")
    member_type: TenantUserInviteMemberType = Field(description="Tipo de membro")
    status: TenantUserInviteStatusEnum = Field(description="Status do convite")
    created_at: datetime = Field(description="Data de criação do convite")
    updated_at: datetime = Field(description="Data de atualização do convite")
