from uuid import UUID

from fastapi_pagination import Page

from app.enums.models.hospitalization_status_enums import HospitalizationStatus
from app.models.hospitalization import Hospitalization
from app.modules.hospitalization.dtos.hospitalization.create_hospitalization_dto import (
    CreateHospitalizationDTO,
)
from app.modules.hospitalization.dtos.responses.hospitalization.hospitalization_response import (
    HospitalizationResponse,
)
from app.modules.hospitalization.dtos.responses.hospitalization.paginate_hospitalization_response import (
    PaginateHospitalizationResponse,
)
from app.modules.hospitalization.dtos.responses.hospitalization.patient_response import (
    PatientResponse,
)


class HospitalizationMapper:
    def __init__(self, tenant_id: UUID, user_id: UUID) -> None:
        self.tenant_id = tenant_id
        self.user_id = user_id

    def to_entity(self, data: CreateHospitalizationDTO) -> Hospitalization:
        return Hospitalization(
            tenant_id=self.tenant_id,
            user_id=self.user_id,
            patient_id=data.patient_id,
            medical_team_id=data.medical_team_id,
            status=HospitalizationStatus.ACTIVE,
            hospitalization_number=data.number,
            hospitalization_place=data.place,
            hospitalization_sector=data.sector,
            hospitalization_reason=data.reason,
            observation=data.observation,
        )

    @staticmethod
    def to_response(data: Hospitalization) -> HospitalizationResponse:
        patient = PatientResponse(
            id=data.patient.id,
            first_name=data.patient.first_name,
            last_name=data.patient.last_name,
        )
        return HospitalizationResponse(
            id=data.id,
            user_id=data.user_id,
            patient_id=data.patient_id,
            patient=patient,
            medical_team_id=data.medical_team_id,
            status=data.status,
            number=data.hospitalization_number,
            place=data.hospitalization_place,
            sector=data.hospitalization_sector,
            reason=data.hospitalization_reason,
            observation=data.observation,
            created_at=data.created_at,
            updated_at=data.updated_at,
        )

    @staticmethod
    def to_paginate_response(
        data: Page[Hospitalization],
    ) -> PaginateHospitalizationResponse:
        items = [
            HospitalizationMapper.to_response(hospitalization)
            for hospitalization in data.items
        ]
        return PaginateHospitalizationResponse(
            data=items,
            total=data.total,
            page=data.page,
            limit=data.size,
            total_pages=data.pages,
        )
