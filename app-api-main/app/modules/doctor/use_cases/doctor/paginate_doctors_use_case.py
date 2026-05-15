from app.modules.doctor.dtos.doctor.paginate_doctors_dto import PaginateDoctorsDTO
from app.modules.doctor.dtos.responses.doctor.paginate_doctors_response import (
    PaginateDoctorsResponseDTO,
)
from app.modules.doctor.mappers.doctor_mapper import DoctorMapper
from app.modules.doctor.repositories.doctor_repository import DoctorRepository


class PaginateDoctorsUseCase:
    def __init__(
        self,
        doctor_repository: DoctorRepository,
        doctor_mapper: DoctorMapper,
    ) -> None:
        self.doctor_repository = doctor_repository
        self.doctor_mapper = doctor_mapper

    def handle(self, params: PaginateDoctorsDTO) -> PaginateDoctorsResponseDTO:
        pagination = self.doctor_repository.paginate(
            page=params.page,
            limit=params.limit,
            search=params.search,
        )
        return self.doctor_mapper.to_paginate_response(pagination)
