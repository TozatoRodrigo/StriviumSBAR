from typing import Annotated
from uuid import UUID

from fastapi import Depends, status
from fastapi.responses import JSONResponse

from app.modules.tenant_user.di.tenant_user_invite.use_cases import (
    get_accept_invite_use_case,
    get_get_invites_use_case,
    get_get_pending_invites_count_use_case,
    get_get_tenant_pending_invites_use_case,
    get_reject_invite_use_case,
    get_send_invite_use_case,
)
from app.modules.tenant_user.dtos.tenant_user_invite.create_tenant_user_invite_dto import (
    CreateTenantUserInviteDTO,
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


def send_invite(
    data: CreateTenantUserInviteDTO,
    use_case: Annotated[SendInviteUseCase, Depends(get_send_invite_use_case)],
) -> JSONResponse:
    use_case.handle(data)
    return JSONResponse(content=None, status_code=status.HTTP_202_ACCEPTED)


def get_tenant_pending_invites(
    use_case: Annotated[
        GetTenantPendingInvitesUseCase, Depends(get_get_tenant_pending_invites_use_case)
    ],
) -> JSONResponse:
    result = use_case.handle()
    return JSONResponse(content=result.to_json(), status_code=status.HTTP_200_OK)


def get_pending_invites(
    use_case: Annotated[GetInvitesUseCase, Depends(get_get_invites_use_case)],
) -> JSONResponse:
    result = use_case.handle()
    return JSONResponse(content=result.to_json(), status_code=status.HTTP_200_OK)


def accept_invite(
    invite_id: UUID,
    use_case: Annotated[AcceptInviteUseCase, Depends(get_accept_invite_use_case)],
) -> JSONResponse:
    result = use_case.handle(invite_id)
    return JSONResponse(content=result.to_json(), status_code=status.HTTP_200_OK)


def get_pending_invites_count(
    use_case: Annotated[
        GetPendingInvitesCountUseCase, Depends(get_get_pending_invites_count_use_case)
    ],
) -> JSONResponse:
    result = use_case.handle()
    return JSONResponse(content=result.to_json(), status_code=status.HTTP_200_OK)


def reject_invite(
    invite_id: UUID,
    use_case: Annotated[RejectInviteUseCase, Depends(get_reject_invite_use_case)],
) -> JSONResponse:
    result = use_case.handle(invite_id)
    return JSONResponse(content=result.to_json(), status_code=status.HTTP_200_OK)
