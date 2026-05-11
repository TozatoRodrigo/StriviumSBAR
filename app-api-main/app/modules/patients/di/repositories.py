from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlmodel import Session

from app.core.database import get_session
from app.modules.patients.repositories.patient_repository import PatientRepository
from app.services.tenant.tenant_service import get_tenant_id_from_token


def get_patient_repository(
    session: Annotated[Session, Depends(get_session)],
    tenant_id: Annotated[UUID, Depends(get_tenant_id_from_token)],
) -> PatientRepository:
    return PatientRepository(session, tenant_id)
