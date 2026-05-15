import logging
from enum import StrEnum

from fastapi import status

from app.core.environment import envs
from app.exceptions.client_aware_error import ClientAwareError
from app.infrastructure.email.dto.send_mail_dto import SendMailDTO
from app.infrastructure.email.send_mail import SendMail
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

log = logging.getLogger("logger")


class InviteEmailDispatchStatus(StrEnum):
    SKIPPED = "skipped"
    SENT = "sent"


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

    def handle(
        self, create_tenant_user_invite_dto: CreateTenantUserInviteDTO
    ) -> InviteEmailDispatchStatus:
        tenant_user_invite = self.tenant_user_invite_mapper.to_model(
            create_tenant_user_invite_dto
        )
        self.__validate_invite(tenant_user_invite)
        tenant_user_invite = self.tenant_user_invite_repository.save(tenant_user_invite)
        return self.__send_invite_email(tenant_user_invite)

    @staticmethod
    def __send_invite_email(
        tenant_user_invite: TenantUserInvite,
    ) -> InviteEmailDispatchStatus:
        if not envs.TENANT_INVITE_EMAIL_ENABLED:
            log.info(
                "Tenant invite email dispatch disabled by configuration",
                extra={
                    "event": "tenant_user_invite.email_disabled",
                    "invite_id": str(tenant_user_invite.id),
                    "invite_email": tenant_user_invite.email,
                },
            )
            return InviteEmailDispatchStatus.SKIPPED

        mail = SendMail()
        subject = "Convite para acessar o Strivium"
        body = (
            "Você recebeu um convite para acessar o Strivium. "
            f"ID do convite: {tenant_user_invite.id}"
        )
        try:
            mail.send(
                SendMailDTO(
                    destination=tenant_user_invite.email,
                    subject=subject,
                    body=body,
                )
            )
            return InviteEmailDispatchStatus.SENT
        except Exception as exc:
            log.exception(
                "Failed to send tenant invite email",
                extra={
                    "event": "tenant_user_invite.email_send_failed",
                    "invite_id": str(tenant_user_invite.id),
                    "invite_email": tenant_user_invite.email,
                },
            )
            message = "Não foi possível enviar o e-mail de convite no momento"
            raise ClientAwareError(
                message, status.HTTP_503_SERVICE_UNAVAILABLE
            ) from exc

    def __validate_invite(self, tenant_user_invite: TenantUserInvite) -> None:
        if tenant_user_invite.email == self.current_user.email:
            msg = "Invite is for the current user"
            raise InvalidInviteError(msg)
