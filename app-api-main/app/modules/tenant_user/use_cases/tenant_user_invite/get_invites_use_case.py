from app.models.user import User
from app.modules.tenant_user.dtos.responses.tenant_user_invite.list_tenant_user_invite_response import (
    ListTenantUserInviteResponse,
)
from app.modules.tenant_user.mappers.tenant_user_invite_mapper import (
    TenantUserInviteMapper,
)
from app.modules.tenant_user.repositories.tenant_user_invite_repository import (
    TenantUserInviteRepository,
)


class GetInvitesUseCase:
    def __init__(
        self,
        tenant_user_invite_repository: TenantUserInviteRepository,
        tenant_user_invite_mapper: TenantUserInviteMapper,
        current_user: User,
    ) -> None:
        self.tenant_user_invite_repository = tenant_user_invite_repository
        self.tenant_user_invite_mapper = tenant_user_invite_mapper
        self.current_user = current_user

    def handle(self) -> ListTenantUserInviteResponse:
        data = self.tenant_user_invite_repository.list_pendings_by_email(
            self.current_user.email
        )
        return self.tenant_user_invite_mapper.to_list_response(data)
