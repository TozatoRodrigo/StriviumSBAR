from sqlmodel import Session, select

from app.enums.models.hospitalization_status_enums import HospitalizationStatus
from app.exceptions.validation_error import ValidationError
from app.models.hospitalization import Hospitalization
from app.modules.hospitalization.dtos.hospitalization.create_hospitalization_dto import (
    CreateHospitalizationDTO,
)
from app.modules.hospitalization.validations.create_hospitalization.base_validation import (
    BaseValidation,
)


class DuplicatedHospitalizationValidation(BaseValidation):
    def __init__(self, session: Session) -> None:
        self.session = session

    def validate(self, data: CreateHospitalizationDTO) -> None:
        hospitalization = self.session.exec(
            select(Hospitalization).where(
                Hospitalization.patient_id == data.patient_id,
                Hospitalization.medical_team_id == data.medical_team_id,
                Hospitalization.status == HospitalizationStatus.ACTIVE,
            )
        ).first()
        if hospitalization:
            msg = "Paciente já possui uma internação ativa nessa equipe"
            raise ValidationError(msg)
