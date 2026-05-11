from uuid import UUID

from app.modules.hospitalization.dtos.responses.hospitalization.paginate_hospitalization_response import (
    PaginateHospitalizationResponse,
)
from app.modules.hospitalization.mappers.hospitalization_mapper import (
    HospitalizationMapper,
)
from app.modules.hospitalization.repositories.hospitalization_repository import (
    HospitalizationRepository,
)


class PaginateHospitalizationsUseCase:
    def __init__(
        self,
        repository: HospitalizationRepository,
        mapper: HospitalizationMapper,
    ) -> None:
        self.repository = repository
        self.mapper = mapper

    def handle(
        self,
        page: int,
        limit: int,
        patient_id: UUID | None = None,
        search: str | None = None,
    ) -> PaginateHospitalizationResponse:
        pagination = self.repository.paginate(page, limit, patient_id, search)
        return self.mapper.to_paginate_response(pagination)
