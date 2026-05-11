from uuid import UUID

from fastapi_pagination import Page

from app.models.patient import Patient
from app.modules.patients.dtos.patient.create_patient_dto import CreatePatientDTO
from app.modules.patients.dtos.responses.patient.paginate_patients_response_dto import (
    PaginatePatientsResponseDTO,
)
from app.modules.patients.dtos.responses.patient.patient_response_dto import (
    PatientResponseDTO,
)


class PatientMapper:
    def __init__(self, tenant_id: UUID) -> None:
        self.tenant_id = tenant_id

    def to_entity(self, data: CreatePatientDTO) -> Patient:
        return Patient(
            tenant_id=self.tenant_id,
            first_name=data.first_name,
            last_name=data.last_name,
            document_number=data.document_number,
            birth_date=data.birth_date,
        )

    @staticmethod
    def to_response(patient: Patient) -> PatientResponseDTO:
        return PatientResponseDTO(
            id=patient.id,
            first_name=patient.first_name,
            last_name=patient.last_name,
            document_number=patient.document_number,
            birth_date=patient.birth_date,
            created_at=patient.created_at,
            updated_at=patient.updated_at,
        )

    @staticmethod
    def to_paginate_response(pagination: Page[Patient]) -> PaginatePatientsResponseDTO:
        items = [PatientMapper.to_response(patient) for patient in pagination.items]
        return PaginatePatientsResponseDTO(
            data=items,
            total=pagination.total,
            page=pagination.page,
            limit=pagination.size,
            total_pages=pagination.pages,
        )
