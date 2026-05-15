from uuid import UUID

from sqlmodel import Session, select

from app.exceptions.validation_error import ValidationError
from app.models.patient import Patient
from app.modules.hospitalization.dtos.hospitalization.create_hospitalization_dto import (
    CreateHospitalizationDTO,
)
from app.modules.hospitalization.validations.create_hospitalization.base_validation import (
    BaseValidation,
)


class PatientBelongsToTenantValidation(BaseValidation):
    def __init__(self, session: Session, tenant_id: UUID) -> None:
        self.session = session
        self.tenant_id = tenant_id

    def validate(self, data: CreateHospitalizationDTO) -> None:
        patient = self.session.exec(
            select(Patient).where(
                Patient.id == data.patient_id,
                Patient.tenant_id == self.tenant_id,
            )
        ).first()
        if patient is None:
            msg = "Paciente não pertence ao tenant autenticado"
            raise ValidationError(msg)
