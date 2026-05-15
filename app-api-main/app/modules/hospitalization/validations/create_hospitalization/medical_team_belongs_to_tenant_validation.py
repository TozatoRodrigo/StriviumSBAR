from uuid import UUID

from sqlmodel import Session, select

from app.exceptions.validation_error import ValidationError
from app.models.medical_team import MedicalTeam
from app.modules.hospitalization.dtos.hospitalization.create_hospitalization_dto import (
    CreateHospitalizationDTO,
)
from app.modules.hospitalization.validations.create_hospitalization.base_validation import (
    BaseValidation,
)


class MedicalTeamBelongsToTenantValidation(BaseValidation):
    def __init__(self, session: Session, tenant_id: UUID) -> None:
        self.session = session
        self.tenant_id = tenant_id

    def validate(self, data: CreateHospitalizationDTO) -> None:
        medical_team = self.session.exec(
            select(MedicalTeam).where(
                MedicalTeam.id == data.medical_team_id,
                MedicalTeam.tenant_id == self.tenant_id,
            )
        ).first()
        if medical_team is None:
            msg = "Equipe médica não pertence ao tenant autenticado"
            raise ValidationError(msg)
