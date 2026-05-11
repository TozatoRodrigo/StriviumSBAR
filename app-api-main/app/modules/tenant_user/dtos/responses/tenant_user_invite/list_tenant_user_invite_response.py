from app.concerns.base_model import BaseModel
from app.modules.tenant_user.dtos.responses.tenant_user_invite.detailed_tenant_user_invite_response import (
    DetailedTenantUserInviteResponse,
)


class ListTenantUserInviteResponse(BaseModel):
    data: list[DetailedTenantUserInviteResponse]
