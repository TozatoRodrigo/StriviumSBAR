from app.modules.hospitalization.dtos.hospitalization.create_hospitalization_dto import (
    CreateHospitalizationDTO,
)
from app.modules.hospitalization.dtos.responses.hospitalization.hospitalization_response import (
    HospitalizationResponse,
)
from app.modules.hospitalization.mappers.hospitalization_mapper import (
    HospitalizationMapper,
)
from app.modules.hospitalization.repositories.hospitalization_action_repository import (
    HospitalizationActionRepository,
)
from app.modules.hospitalization.repositories.hospitalization_repository import (
    HospitalizationRepository,
)
from app.modules.hospitalization.validations.create_hospitalization.base_validation import (
    BaseValidation,
)


class CreateHospitalizationUseCase:
    def __init__(
        self,
        repository: HospitalizationRepository,
        mapper: HospitalizationMapper,
        hospitalization_action_repository: HospitalizationActionRepository,
        validations: list[BaseValidation],
    ) -> None:
        self.repository = repository
        self.mapper = mapper
        self.hospitalization_action_repository = hospitalization_action_repository
        self.validations = validations

    def handle(self, data: CreateHospitalizationDTO) -> HospitalizationResponse:
        self.__validate(data)
        hospitalization_entity = self.mapper.to_entity(data)
        hospitalization = self.repository.save(hospitalization_entity)
        return self.mapper.to_response(hospitalization)

    def __validate(self, data: CreateHospitalizationDTO) -> None:
        for validation in self.validations:
            validation.validate(data)
