from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.core.database import get_session
from app.modules.hospitalization.repositories.hospitalization_action_attachment_repository import (
    HospitalizationActionAttachmentRepository,
)


def get_hospitalization_action_attachment_repository(
    session: Annotated[Session, Depends(get_session)],
) -> HospitalizationActionAttachmentRepository:
    return HospitalizationActionAttachmentRepository(session)
