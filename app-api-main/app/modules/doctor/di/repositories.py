from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlmodel import Session

from app.core.database import get_session
from app.modules.doctor.repositories.doctor_repository import DoctorRepository
from app.modules.doctor.repositories.role_repository import RoleRepository
from app.services.tenant.tenant_service import get_tenant_id_from_token


def get_doctor_repository(
    session: Annotated[Session, Depends(get_session)],
    tenant_id: Annotated[UUID, Depends(get_tenant_id_from_token)],
) -> DoctorRepository:
    return DoctorRepository(session, tenant_id)


def get_role_repository(
    session: Annotated[Session, Depends(get_session)],
) -> RoleRepository:
    return RoleRepository(session)
