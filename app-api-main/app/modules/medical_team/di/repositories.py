from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlmodel import Session

from app.core.database import get_session
from app.modules.medical_team.repositories.medical_team_repository import (
    MedicalTeamRepository,
)
from app.services.tenant.tenant_service import get_tenant_id_from_token


def get_medical_team_repository(
    session: Annotated[Session, Depends(get_session)],
    tenant_id: Annotated[UUID, Depends(get_tenant_id_from_token)],
) -> MedicalTeamRepository:
    return MedicalTeamRepository(session, tenant_id)
