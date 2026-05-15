from fastapi import APIRouter, Depends, status

from app.enums.models.permissions_enums import TenantUserPermissionsEnum
from app.middlewares.auth_middleware import (
    require_permission,
    verify_tenant_jwt,
    verify_user_jwt,
)
from app.modules.tenant_user.controllers.tenant_user_controller import (
    paginate_tenant_users,
)
from app.modules.tenant_user.controllers.tenant_user_invite_controller import (
    accept_invite,
    get_pending_invites,
    get_pending_invites_count,
    get_tenant_pending_invites,
    reject_invite,
    send_invite,
)
from app.modules.tenant_user.dtos.responses.tenant_user.paginate_tenant_users_response import (
    PaginateTenantUsersResponse,
)
from app.modules.tenant_user.dtos.responses.tenant_user_invite.list_tenant_user_invite_response import (
    ListTenantUserInviteResponse,
)
from app.modules.tenant_user.dtos.responses.tenant_user_invite.pending_invites_count_response import (
    PendingInvitesCountResponse,
)
from app.modules.tenant_user.dtos.responses.tenant_user_invite.tenant_user_invite_response import (
    TenantUserInviteResponse,
)

router = APIRouter(prefix="/tenant-user/v1/tenant-users", tags=["tenant-user"])

router.add_api_route(
    "",
    endpoint=paginate_tenant_users,
    methods=["GET"],
    status_code=status.HTTP_200_OK,
    response_model=PaginateTenantUsersResponse,
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(TenantUserPermissionsEnum.READ.value)),
    ],
)

router.add_api_route(
    "/invite",
    endpoint=send_invite,
    methods=["POST"],
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(TenantUserPermissionsEnum.CREATE.value)),
    ],
    status_code=status.HTTP_202_ACCEPTED,
)

router.add_api_route(
    "/invites",
    endpoint=get_tenant_pending_invites,
    methods=["GET"],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(verify_tenant_jwt),
        Depends(require_permission(TenantUserPermissionsEnum.READ.value)),
    ],
    response_model=ListTenantUserInviteResponse,
)

router.add_api_route(
    "/pending-invites",
    endpoint=get_pending_invites,
    methods=["GET"],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_user_jwt)],
    response_model=ListTenantUserInviteResponse,
)

router.add_api_route(
    "/accept-invite/{invite_id}",
    endpoint=accept_invite,
    methods=["POST"],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_user_jwt)],
    response_model=TenantUserInviteResponse,
)

router.add_api_route(
    "/reject-invite/{invite_id}",
    endpoint=reject_invite,
    methods=["POST"],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_user_jwt)],
    response_model=TenantUserInviteResponse,
)

router.add_api_route(
    "/pending-invites/count",
    endpoint=get_pending_invites_count,
    methods=["GET"],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_user_jwt)],
    response_model=PendingInvitesCountResponse,
)
