from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.modules.hospitalization.repositories.hospitalization_repository import (
    HospitalizationRepository,
)
from app.services.tenant.tenant_service import get_tenant_id_from_token


def get_hospitalization_repository(
    session: Annotated[Session, Depends(get_session)],
    tenant_id: Annotated[UUID, Depends(get_tenant_id_from_token)],
) -> HospitalizationRepository:
    return HospitalizationRepository(session, tenant_id)
