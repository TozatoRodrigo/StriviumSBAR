from uuid import UUID

from pydantic import BaseModel, Field

from app.enums.models.tenant_user_invite_member_type_enums import (
    TenantUserInviteMemberType,
)


class CreateTenantUserInviteDTO(BaseModel):
    email: str = Field(..., description="The email of the user to invite")
    member_type: TenantUserInviteMemberType | None = Field(
        default=None,
        description="The member type of the user to invite",
    )
    role_id: UUID = Field(..., description="The role of the user to invite")
