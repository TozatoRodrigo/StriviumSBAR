from uuid import UUID

from app.enums.models.tenant_user_invite_status_enum import TenantUserInviteStatusEnum
from app.models.tenant_user_invite import TenantUserInvite
from app.models.user import User
from app.modules.tenant_user.dtos.responses.tenant_user_invite.tenant_user_invite_response import (
    TenantUserInviteResponse,
)
from app.modules.tenant_user.exceptions.invalid_invite_error import InvalidInviteError
from app.modules.tenant_user.mappers.tenant_user_invite_mapper import (
    TenantUserInviteMapper,
)
from app.modules.tenant_user.repositories.tenant_user_invite_repository import (
    TenantUserInviteRepository,
)


class RejectInviteUseCase:
    def __init__(
        self,
        tenant_user_invite_repository: TenantUserInviteRepository,
        tenant_user_invite_mapper: TenantUserInviteMapper,
        current_user: User,
    ) -> None:
        self.tenant_user_invite_repository = tenant_user_invite_repository
        self.tenant_user_invite_mapper = tenant_user_invite_mapper
        self.current_user = current_user

    def handle(self, invite_id: UUID) -> TenantUserInviteResponse:
        tenant_user_invite = self.tenant_user_invite_repository.get_by_id(invite_id)
        self.__validate_invite(tenant_user_invite)

        tenant_user_invite.status = TenantUserInviteStatusEnum.REJECTED
        tenant_user_invite = self.tenant_user_invite_repository.save(tenant_user_invite)
        return self.tenant_user_invite_mapper.to_response(tenant_user_invite)

    def __validate_invite(self, tenant_user_invite: TenantUserInvite | None) -> None:
        if tenant_user_invite is None:
            msg = "Invite not found"
            raise InvalidInviteError(msg)
        if tenant_user_invite.status != TenantUserInviteStatusEnum.PENDING:
            msg = "Invite is not pending"
            raise InvalidInviteError(msg)
        if tenant_user_invite.email != self.current_user.email:
            msg = "Invite is not for the current user"
            raise InvalidInviteError(msg)
