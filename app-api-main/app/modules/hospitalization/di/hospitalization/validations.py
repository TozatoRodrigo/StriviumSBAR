from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlmodel import Session

from app.core.database import get_session
from app.modules.hospitalization.validations.create_hospitalization.base_validation import (
    BaseValidation,
)
from app.modules.hospitalization.validations.create_hospitalization.duplicated_hospitalization_validation import (
    DuplicatedHospitalizationValidation,
)
from app.modules.hospitalization.validations.create_hospitalization.medical_team_belongs_to_tenant_validation import (
    MedicalTeamBelongsToTenantValidation,
)
from app.modules.hospitalization.validations.create_hospitalization.patient_belongs_to_tenant_validation import (
    PatientBelongsToTenantValidation,
)
from app.services.tenant.tenant_service import get_tenant_id_from_token


def get_create_hospitalization_validations(
    session: Annotated[Session, Depends(get_session)],
    tenant_id: Annotated[UUID, Depends(get_tenant_id_from_token)],
) -> list[BaseValidation]:
    return [
        PatientBelongsToTenantValidation(session, tenant_id),
        MedicalTeamBelongsToTenantValidation(session, tenant_id),
        DuplicatedHospitalizationValidation(session, tenant_id),
    ]
