from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.di.services import (
    get_logged_user,
    get_logged_user_by_tenant_token,
)
from app.models.user import User
from app.modules.tenant_user.di.tenant_user.repositories import (
    get_tenant_user_repository,
)
from app.modules.tenant_user.di.tenant_user_invite.mappers import (
    get_tenant_user_invite_mapper,
)
from app.modules.tenant_user.di.tenant_user_invite.repositories import (
    get_tenant_user_invite_repository,
)
from app.modules.tenant_user.mappers.tenant_user_invite_mapper import (
    TenantUserInviteMapper,
)
from app.modules.tenant_user.repositories.tenant_user_invite_repository import (
    TenantUserInviteRepository,
)
from app.modules.tenant_user.repositories.tenant_user_repository import (
    TenantUserRepository,
)
from app.modules.tenant_user.use_cases.tenant_user_invite.accept_invite_use_case import (
    AcceptInviteUseCase,
)
from app.modules.tenant_user.use_cases.tenant_user_invite.get_invites_use_case import (
    GetInvitesUseCase,
)
from app.modules.tenant_user.use_cases.tenant_user_invite.get_pending_invites_count_use_case import (
    GetPendingInvitesCountUseCase,
)
from app.modules.tenant_user.use_cases.tenant_user_invite.get_tenant_pending_invites_use_case import (
    GetTenantPendingInvitesUseCase,
)
from app.modules.tenant_user.use_cases.tenant_user_invite.reject_invite_use_case import (
    RejectInviteUseCase,
)
from app.modules.tenant_user.use_cases.tenant_user_invite.send_invite_use_case import (
    SendInviteUseCase,
)
from app.services.tenant.tenant_service import get_tenant_id_from_token


def get_send_invite_use_case(
    tenant_user_invite_repository: Annotated[
        TenantUserInviteRepository, Depends(get_tenant_user_invite_repository)
    ],
    tenant_user_invite_mapper: Annotated[
        TenantUserInviteMapper, Depends(get_tenant_user_invite_mapper)
    ],
    current_user: Annotated[User, Depends(get_logged_user_by_tenant_token)],
) -> SendInviteUseCase:
    return SendInviteUseCase(
        tenant_user_invite_repository,
        tenant_user_invite_mapper,
        current_user,
    )


def get_get_invites_use_case(
    tenant_user_invite_repository: Annotated[
        TenantUserInviteRepository, Depends(get_tenant_user_invite_repository)
    ],
    tenant_user_invite_mapper: Annotated[
        TenantUserInviteMapper, Depends(get_tenant_user_invite_mapper)
    ],
    current_user: Annotated[User, Depends(get_logged_user)],
) -> GetInvitesUseCase:
    return GetInvitesUseCase(
        tenant_user_invite_repository,
        tenant_user_invite_mapper,
        current_user,
    )


def get_accept_invite_use_case(
    tenant_user_invite_repository: Annotated[
        TenantUserInviteRepository, Depends(get_tenant_user_invite_repository)
    ],
    tenant_user_invite_mapper: Annotated[
        TenantUserInviteMapper, Depends(get_tenant_user_invite_mapper)
    ],
    tenant_user_repository: Annotated[
        TenantUserRepository, Depends(get_tenant_user_repository)
    ],
    current_user: Annotated[User, Depends(get_logged_user)],
) -> AcceptInviteUseCase:
    return AcceptInviteUseCase(
        tenant_user_invite_repository,
        tenant_user_invite_mapper,
        tenant_user_repository,
        current_user,
    )


def get_get_pending_invites_count_use_case(
    tenant_user_invite_repository: Annotated[
        TenantUserInviteRepository, Depends(get_tenant_user_invite_repository)
    ],
    tenant_user_invite_mapper: Annotated[
        TenantUserInviteMapper, Depends(get_tenant_user_invite_mapper)
    ],
    current_user: Annotated[User, Depends(get_logged_user)],
) -> GetPendingInvitesCountUseCase:
    return GetPendingInvitesCountUseCase(
        tenant_user_invite_repository,
        tenant_user_invite_mapper,
        current_user,
    )


def get_reject_invite_use_case(
    tenant_user_invite_repository: Annotated[
        TenantUserInviteRepository, Depends(get_tenant_user_invite_repository)
    ],
    tenant_user_invite_mapper: Annotated[
        TenantUserInviteMapper, Depends(get_tenant_user_invite_mapper)
    ],
    current_user: Annotated[User, Depends(get_logged_user)],
) -> RejectInviteUseCase:
    return RejectInviteUseCase(
        tenant_user_invite_repository,
        tenant_user_invite_mapper,
        current_user,
    )


def get_get_tenant_pending_invites_use_case(
    tenant_user_invite_repository: Annotated[
        TenantUserInviteRepository, Depends(get_tenant_user_invite_repository)
    ],
    tenant_user_invite_mapper: Annotated[
        TenantUserInviteMapper, Depends(get_tenant_user_invite_mapper)
    ],
    tenant_id: Annotated[UUID, Depends(get_tenant_id_from_token)],
) -> GetTenantPendingInvitesUseCase:
    return GetTenantPendingInvitesUseCase(
        tenant_user_invite_repository,
        tenant_user_invite_mapper,
        tenant_id,
    )
