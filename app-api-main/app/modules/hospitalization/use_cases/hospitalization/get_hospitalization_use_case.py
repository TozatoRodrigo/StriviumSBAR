from uuid import UUID

from app.modules.hospitalization.dtos.responses.hospitalization.hospitalization_response import (
    HospitalizationResponse,
)
from app.modules.hospitalization.mappers.hospitalization_mapper import (
    HospitalizationMapper,
)
from app.modules.hospitalization.repositories.hospitalization_repository import (
    HospitalizationRepository,
)


class GetHospitalizationUseCase:
    def __init__(
        self, repository: HospitalizationRepository, mapper: HospitalizationMapper
    ) -> None:
        self.repository = repository
        self.mapper = mapper

    def handle(self, hospitalization_id: UUID) -> HospitalizationResponse:
        hospitalization = self.repository.get(hospitalization_id)
        return self.mapper.to_response(hospitalization)
