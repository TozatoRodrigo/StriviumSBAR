from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.core.database import get_session
from app.modules.hospitalization.validations.create_hospitalization.base_validation import (
    BaseValidation,
)
from app.modules.hospitalization.validations.create_hospitalization.duplicated_hospitalization_validation import (
    DuplicatedHospitalizationValidation,
)


def get_create_hospitalization_validations(
    session: Annotated[Session, Depends(get_session)],
) -> list[BaseValidation]:
    return [DuplicatedHospitalizationValidation(session)]
