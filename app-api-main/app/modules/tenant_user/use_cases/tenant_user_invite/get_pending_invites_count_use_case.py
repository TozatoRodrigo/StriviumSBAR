from app.models.user import User
from app.modules.tenant_user.dtos.responses.tenant_user_invite.pending_invites_count_response import (
    PendingInvitesCountResponse,
)
from app.modules.tenant_user.mappers.tenant_user_invite_mapper import (
    TenantUserInviteMapper,
)
from app.modules.tenant_user.repositories.tenant_user_invite_repository import (
    TenantUserInviteRepository,
)


class GetPendingInvitesCountUseCase:
    def __init__(
        self,
        tenant_user_invite_repository: TenantUserInviteRepository,
        mapper: TenantUserInviteMapper,
        current_user: User,
    ) -> None:
        self.tenant_user_invite_repository = tenant_user_invite_repository
        self.mapper = mapper
        self.current_user = current_user

    def handle(self) -> PendingInvitesCountResponse:
        count = self.tenant_user_invite_repository.get_pending_invites_count_by_email(
            self.current_user.email
        )
        return self.mapper.to_count_response(count)
