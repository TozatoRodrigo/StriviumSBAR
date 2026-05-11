from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.modules.tenant_user.mappers.tenant_user_invite_mapper import (
    TenantUserInviteMapper,
)
from app.services.tenant.tenant_service import get_tenant_id_from_token


def get_tenant_user_invite_mapper(
    tenant_id: Annotated[UUID, Depends(get_tenant_id_from_token)],
) -> TenantUserInviteMapper:
    return TenantUserInviteMapper(tenant_id)
