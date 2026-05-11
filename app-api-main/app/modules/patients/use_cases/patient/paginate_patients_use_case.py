from app.modules.patients.dtos.patient.paginate_patients_dto import PaginatePatientsDTO
from app.modules.patients.dtos.responses.patient.paginate_patients_response_dto import (
    PaginatePatientsResponseDTO,
)
from app.modules.patients.mappers.patient_mapper import PatientMapper
from app.modules.patients.repositories.patient_repository import PatientRepository


class PaginatePatientsUseCase:
    def __init__(
        self,
        patient_repository: PatientRepository,
        patient_mapper: PatientMapper,
    ) -> None:
        self.patient_repository = patient_repository
        self.patient_mapper = patient_mapper

    def handle(self, params: PaginatePatientsDTO) -> PaginatePatientsResponseDTO:
        pagination = self.patient_repository.paginate(
            params.page, params.limit, params.search
        )
        return self.patient_mapper.to_paginate_response(pagination)
