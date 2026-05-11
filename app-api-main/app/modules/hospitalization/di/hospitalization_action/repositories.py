from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlmodel import Session

from app.core.database import get_session
from app.modules.hospitalization.repositories.hospitalization_action_attachment_repository import (
    HospitalizationActionAttachmentRepository,
)
from app.modules.hospitalization.repositories.hospitalization_action_repository import (
    HospitalizationActionRepository,
)
from app.modules.hospitalization.repositories.hospitalization_action_sbar_repository import (
    HospitalizationActionSbarRepository,
)
from app.services.tenant.tenant_service import get_tenant_id_from_token


def get_hospitalization_action_repository(
    session: Annotated[Session, Depends(get_session)],
    tenant_id: Annotated[UUID, Depends(get_tenant_id_from_token)],
) -> HospitalizationActionRepository:
    return HospitalizationActionRepository(session, tenant_id)


def get_hospitalization_action_attachment_repository(
    session: Annotated[Session, Depends(get_session)],
) -> HospitalizationActionAttachmentRepository:
    return HospitalizationActionAttachmentRepository(session)


def get_hospitalization_action_sbar_repository(
    session: Annotated[Session, Depends(get_session)],
    tenant_id: Annotated[UUID, Depends(get_tenant_id_from_token)],
) -> HospitalizationActionSbarRepository:
    return HospitalizationActionSbarRepository(session, tenant_id)
