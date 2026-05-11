from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.modules.medical_team.mappers.medical_team_mapper import MedicalTeamMapper
from app.services.tenant.tenant_service import get_tenant_id_from_token


def get_medical_team_mapper(
    tenant_id: Annotated[UUID, Depends(get_tenant_id_from_token)],
) -> MedicalTeamMapper:
    return MedicalTeamMapper(tenant_id)
