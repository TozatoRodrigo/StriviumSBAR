from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.modules.doctor.mappers.doctor_mapper import DoctorMapper
from app.services.tenant.tenant_service import get_tenant_id_from_token


def get_doctor_mapper(
    tenant_id: Annotated[UUID, Depends(get_tenant_id_from_token)],
) -> DoctorMapper:
    return DoctorMapper(tenant_id)
