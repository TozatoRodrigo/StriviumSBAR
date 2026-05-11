from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.di.services import get_user_id_from_tenant_token
from app.modules.hospitalization.mappers.hospitalization_action_mapper import (
    HospitalizationActionMapper,
)
from app.modules.hospitalization.services.hospitalization.hospitalization_service import (
    get_hospitalization_id_from_path,
)
from app.services.tenant.tenant_service import get_tenant_id_from_token


def get_hospitalization_action_mapper(
    tenant_id: Annotated[UUID, Depends(get_tenant_id_from_token)],
    hospitalization_id: Annotated[UUID, Depends(get_hospitalization_id_from_path)],
    user_id: Annotated[UUID, Depends(get_user_id_from_tenant_token)],
) -> HospitalizationActionMapper:
    return HospitalizationActionMapper(tenant_id, user_id, hospitalization_id)
