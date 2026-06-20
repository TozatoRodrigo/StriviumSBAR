from app.models.tenant_user_invite import TenantUserInvite
from app.models.user import User
from app.modules.tenant_user.dtos.tenant_user_invite.create_tenant_user_invite_dto import (
    CreateTenantUserInviteDTO,
)
from app.modules.tenant_user.exceptions.invalid_invite_error import InvalidInviteError
from app.modules.tenant_user.mappers.tenant_user_invite_mapper import (
    TenantUserInviteMapper,
)
from app.modules.tenant_user.repositories.tenant_user_invite_repository import (
    TenantUserInviteRepository,
)


class SendInviteUseCase:
    def __init__(
        self,
        tenant_user_invite_repository: TenantUserInviteRepository,
        tenant_user_invite_mapper: TenantUserInviteMapper,
        current_user: User,
    ) -> None:
        self.tenant_user_invite_repository = tenant_user_invite_repository
        self.tenant_user_invite_mapper = tenant_user_invite_mapper
        self.current_user = current_user

    def handle(self, create_tenant_user_invite_dto: CreateTenantUserInviteDTO) -> None:
        tenant_user_invite = self.tenant_user_invite_mapper.to_model(
            create_tenant_user_invite_dto
        )
        self.__validate_invite(tenant_user_invite)
        tenant_user_invite = self.tenant_user_invite_repository.save(tenant_user_invite)
        self.__send_invite_email(tenant_user_invite)

    def __send_invite_email(self, tenant_user_invite: TenantUserInvite) -> None:
        pass

    def __validate_invite(self, tenant_user_invite: TenantUserInvite) -> None:
        if tenant_user_invite.email == self.current_user.email:
            msg = "Invite is for the current user"
            raise InvalidInviteError(msg)
