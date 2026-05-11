from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.di.services import get_user_id_from_tenant_token
from app.modules.hospitalization.mappers.hospitalization_mapper import (
    HospitalizationMapper,
)
from app.services.tenant.tenant_service import get_tenant_id_from_token


def get_hospitalization_mapper(
    tenant_id: Annotated[UUID, Depends(get_tenant_id_from_token)],
    user_id: Annotated[UUID, Depends(get_user_id_from_tenant_token)],
) -> HospitalizationMapper:
    return HospitalizationMapper(tenant_id, user_id)
