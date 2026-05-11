from typing import Annotated
from uuid import UUID

from fastapi import Path

from app.modules.hospitalization.exceptions.hospitalization.hospitalization_not_found_error import (
    HospitalizationNotFoundError,
)


def get_hospitalization_id_from_path(
    hospitalization_id: Annotated[UUID | None, Path(title="Hospitalization ID")],
) -> UUID:
    if hospitalization_id is None:
        raise HospitalizationNotFoundError(hospitalization_id)
    return hospitalization_id
