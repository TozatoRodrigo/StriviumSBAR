from uuid import UUID

from app.models.tenant_user_invite import TenantUserInvite
from app.modules.tenant_user.dtos.responses.tenant_user_invite.detailed_tenant_user_invite_response import (
    DetailedTenantUserInviteResponse,
)
from app.modules.tenant_user.dtos.responses.tenant_user_invite.list_tenant_user_invite_response import (
    ListTenantUserInviteResponse,
)
from app.modules.tenant_user.dtos.responses.tenant_user_invite.pending_invites_count_response import (
    PendingInvitesCountResponse,
)
from app.modules.tenant_user.dtos.responses.tenant_user_invite.role_response import (
    RoleResponse,
)
from app.modules.tenant_user.dtos.responses.tenant_user_invite.tenant_response import (
    TenantResponse,
)
from app.modules.tenant_user.dtos.responses.tenant_user_invite.tenant_user_invite_response import (
    TenantUserInviteResponse,
)
from app.modules.tenant_user.dtos.tenant_user_invite.create_tenant_user_invite_dto import (
    CreateTenantUserInviteDTO,
)


class TenantUserInviteMapper:
    def __init__(self, tenant_id: UUID) -> None:
        self.tenant_id = tenant_id

    def to_model(
        self,
        create_tenant_user_invite_dto: CreateTenantUserInviteDTO,
    ) -> TenantUserInvite:
        return TenantUserInvite(
            tenant_id=self.tenant_id,
            role_id=create_tenant_user_invite_dto.role_id,
            email=create_tenant_user_invite_dto.email,
            member_type=create_tenant_user_invite_dto.member_type,
        )

    @staticmethod
    def to_detailed_response(
        tenant_user_invite: TenantUserInvite,
    ) -> DetailedTenantUserInviteResponse:
        return DetailedTenantUserInviteResponse(
            id=tenant_user_invite.id,
            tenant_id=tenant_user_invite.tenant_id,
            tenant=TenantResponse(
                id=tenant_user_invite.tenant.id,
                name=tenant_user_invite.tenant.name,
                logo_url=tenant_user_invite.tenant.logo_url,
            ),
            role=RoleResponse(
                name=tenant_user_invite.role.name,
                description=tenant_user_invite.role.description,
            ),
            email=tenant_user_invite.email,
            member_type=tenant_user_invite.member_type,
            status=tenant_user_invite.status,
            created_at=tenant_user_invite.created_at,
            updated_at=tenant_user_invite.updated_at,
        )

    @staticmethod
    def to_response(data: TenantUserInvite) -> TenantUserInviteResponse:
        return TenantUserInviteResponse(
            id=data.id,
            email=data.email,
            member_type=data.member_type,
            status=data.status,
            created_at=data.created_at,
            updated_at=data.updated_at,
        )

    @staticmethod
    def to_list_response(
        data: list[TenantUserInvite],
    ) -> ListTenantUserInviteResponse:
        items = [TenantUserInviteMapper.to_detailed_response(item) for item in data]
        return ListTenantUserInviteResponse(data=items)

    @staticmethod
    def to_count_response(data: int) -> PendingInvitesCountResponse:
        return PendingInvitesCountResponse(count=data)
