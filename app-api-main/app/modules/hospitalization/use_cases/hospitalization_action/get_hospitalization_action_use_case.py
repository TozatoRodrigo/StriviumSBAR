from uuid import UUID

from app.modules.hospitalization.exceptions.hospitalization_action.hospitalization_action_not_found_error import (
    HospitalizationActionNotFoundError,
)
from app.modules.hospitalization.mappers.hospitalization_action_mapper import (
    HospitalizationActionMapper,
)
from app.modules.hospitalization.repositories.hospitalization_action_repository import (
    HospitalizationAction,
    HospitalizationActionRepository,
)


class GetHospitalizationActionUseCase:
    def __init__(
        self,
        repository: HospitalizationActionRepository,
        mapper: HospitalizationActionMapper,
    ) -> None:
        self.repository = repository
        self.mapper = mapper

    def handle(
        self, hospitalization_id: UUID, hospitalization_action_id: UUID
    ) -> HospitalizationAction:
        hospitalization_action = self.repository.find_by_id(hospitalization_action_id)
        if (
            hospitalization_action is None
            or hospitalization_action.hospitalization_id != hospitalization_id
        ):
            raise HospitalizationActionNotFoundError(hospitalization_action_id)
        return self.mapper.to_response(hospitalization_action)
