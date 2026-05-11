from uuid import UUID

from app.modules.tenant_user.dtos.responses.tenant_user_invite.list_tenant_user_invite_response import (
    ListTenantUserInviteResponse,
)
from app.modules.tenant_user.mappers.tenant_user_invite_mapper import (
    TenantUserInviteMapper,
)
from app.modules.tenant_user.repositories.tenant_user_invite_repository import (
    TenantUserInviteRepository,
)


class GetTenantPendingInvitesUseCase:
    def __init__(
        self,
        tenant_user_invite_repository: TenantUserInviteRepository,
        tenant_user_invite_mapper: TenantUserInviteMapper,
        tenant_id: UUID,
    ) -> None:
        self.tenant_user_invite_repository = tenant_user_invite_repository
        self.tenant_user_invite_mapper = tenant_user_invite_mapper
        self.tenant_id = tenant_id

    def handle(self) -> ListTenantUserInviteResponse:
        data = self.tenant_user_invite_repository.list_pendings_by_tenant_id(
            self.tenant_id
        )
        return self.tenant_user_invite_mapper.to_list_response(data)
