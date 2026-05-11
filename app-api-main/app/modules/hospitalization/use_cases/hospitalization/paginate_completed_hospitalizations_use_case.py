from app.modules.hospitalization.dtos.responses.hospitalization.paginate_hospitalization_response import (
    PaginateHospitalizationResponse,
)
from app.modules.hospitalization.mappers.hospitalization_mapper import (
    HospitalizationMapper,
)
from app.modules.hospitalization.repositories.hospitalization_repository import (
    HospitalizationRepository,
)


class PaginateCompletedHospitalizationsUseCase:
    def __init__(
        self,
        repository: HospitalizationRepository,
        mapper: HospitalizationMapper,
    ) -> None:
        self.repository = repository
        self.mapper = mapper

    def handle(self, page: int, limit: int) -> PaginateHospitalizationResponse:
        pagination = self.repository.paginate_completed(page, limit)
        return self.mapper.to_paginate_response(pagination)
