from uuid import UUID

from app.exceptions.validation_error import ValidationError
from app.modules.hospitalization.dtos.hospitalization.update_hospitalization_dto import (
    UpdateHospitalizationDTO,
)
from app.modules.hospitalization.dtos.responses.hospitalization.hospitalization_response import (
    HospitalizationResponse,
)
from app.modules.hospitalization.exceptions.hospitalization.hospitalization_not_found_error import (
    HospitalizationNotFoundError,
)
from app.modules.hospitalization.mappers.hospitalization_mapper import (
    HospitalizationMapper,
)
from app.modules.hospitalization.repositories.hospitalization_repository import (
    HospitalizationRepository,
)


class UpdateHospitalizationUseCase:
    def __init__(
        self,
        repository: HospitalizationRepository,
        mapper: HospitalizationMapper,
    ) -> None:
        self.repository = repository
        self.mapper = mapper

    def handle(
        self, hospitalization_id: UUID, data: UpdateHospitalizationDTO
    ) -> HospitalizationResponse:
        hospitalization = self.repository.get(hospitalization_id)

        if not hospitalization:
            raise HospitalizationNotFoundError(hospitalization_id)

        if not self.repository.is_medical_team_in_tenant(data.medical_team_id):
            msg = "Equipe médica não pertence ao tenant autenticado"
            raise ValidationError(msg)

        hospitalization.medical_team_id = data.medical_team_id
        hospitalization.hospitalization_number = data.number
        hospitalization.hospitalization_place = data.place
        hospitalization.hospitalization_sector = data.sector
        hospitalization.hospitalization_reason = data.reason
        hospitalization.observation = data.observation

        updated_hospitalization = self.repository.update(hospitalization)
        return self.mapper.to_response(updated_hospitalization)
