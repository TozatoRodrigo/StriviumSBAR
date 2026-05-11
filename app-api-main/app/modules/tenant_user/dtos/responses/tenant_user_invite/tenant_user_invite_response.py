from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.concerns.base_model import BaseModel
from app.enums.models.tenant_user_invite_member_type_enums import (
    TenantUserInviteMemberType,
)
from app.enums.models.tenant_user_invite_status_enum import TenantUserInviteStatusEnum


class TenantUserInviteResponse(BaseModel):
    id: UUID = Field(description="ID do convite")
    email: str = Field(description="Email do convite")
    member_type: TenantUserInviteMemberType = Field(description="Tipo de membro")
    status: TenantUserInviteStatusEnum = Field(description="Status do convite")
    created_at: datetime = Field(description="Data de criação do convite")
    updated_at: datetime = Field(description="Data de atualização do convite")
