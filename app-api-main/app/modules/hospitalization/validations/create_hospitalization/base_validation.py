from abc import ABC, abstractmethod

from app.modules.hospitalization.dtos.hospitalization.create_hospitalization_dto import (
    CreateHospitalizationDTO,
)


class BaseValidation(ABC):
    @abstractmethod
    def validate(self, data: CreateHospitalizationDTO) -> None:
        pass
