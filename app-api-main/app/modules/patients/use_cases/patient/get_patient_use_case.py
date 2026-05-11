from uuid import UUID

from app.modules.patients.dtos.responses.patient.patient_response_dto import (
    PatientResponseDTO,
)
from app.modules.patients.exceptions.patient.patient_not_found_error import (
    PatientNotFoundError,
)
from app.modules.patients.mappers.patient_mapper import PatientMapper
from app.modules.patients.repositories.patient_repository import PatientRepository


class GetPatientUseCase:
    def __init__(
        self,
        patient_repository: PatientRepository,
        patient_mapper: PatientMapper,
    ) -> None:
        self.patient_repository = patient_repository
        self.patient_mapper = patient_mapper

    def handle(self, patient_id: UUID) -> PatientResponseDTO:
        patient = self.patient_repository.find_by_id(patient_id)

        if not patient:
            msg = "Paciente não encontrado"
            raise PatientNotFoundError(msg)

        return self.patient_mapper.to_response(patient)
