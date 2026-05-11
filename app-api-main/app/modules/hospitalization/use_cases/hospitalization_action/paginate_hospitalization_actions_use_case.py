from uuid import UUID

from app.modules.hospitalization.dtos.responses.hospitalization_action.paginate_hospitalization_action_response import (
    PaginateHospitalizationActionResponse,
)
from app.modules.hospitalization.mappers.hospitalization_action_mapper import (
    HospitalizationActionMapper,
)
from app.modules.hospitalization.repositories.hospitalization_action_repository import (
    HospitalizationActionRepository,
)


class PaginateHospitalizationActionsUseCase:
    def __init__(
        self,
        hospitalization_action_repository: HospitalizationActionRepository,
        mapper: HospitalizationActionMapper,
    ) -> None:
        self.hospitalization_action_repository = hospitalization_action_repository
        self.mapper = mapper

    def handle(
        self, hospitalization_id: UUID, page: int, limit: int
    ) -> PaginateHospitalizationActionResponse:
        hospitalization_actions = (
            self.hospitalization_action_repository.paginate_by_hospitalization_id(
                hospitalization_id, page, limit
            )
        )
        return self.mapper.to_paginate_response(hospitalization_actions)
