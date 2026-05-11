from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.modules.patients.mappers.patient_mapper import PatientMapper
from app.services.tenant.tenant_service import get_tenant_id_from_token


def get_patient_mapper(
    tenant_id: Annotated[UUID, Depends(get_tenant_id_from_token)],
) -> PatientMapper:
    return PatientMapper(tenant_id)
