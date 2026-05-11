from app.modules.patients.dtos.patient.create_patient_dto import CreatePatientDTO
from app.modules.patients.dtos.responses.patient.patient_response_dto import (
    PatientResponseDTO,
)
from app.modules.patients.mappers.patient_mapper import PatientMapper
from app.modules.patients.repositories.patient_repository import PatientRepository


class CreatePatientUseCase:
    def __init__(
        self,
        patient_repository: PatientRepository,
        patient_mapper: PatientMapper,
    ) -> None:
        self.patient_repository = patient_repository
        self.patient_mapper = patient_mapper

    def handle(self, data: CreatePatientDTO) -> PatientResponseDTO:
        patient_entity = self.patient_mapper.to_entity(data)
        patient = self.patient_repository.save(patient_entity)
        return self.patient_mapper.to_response(patient)
