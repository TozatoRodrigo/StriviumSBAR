from uuid import UUID

from app.modules.doctor.dtos.responses.doctor.detailed_doctor_response import (
    DetailedDoctorResponseDTO,
)
from app.modules.doctor.exceptions.doctor_not_found_error import DoctorNotFoundError
from app.modules.doctor.mappers.doctor_mapper import DoctorMapper
from app.modules.doctor.repositories.doctor_repository import DoctorRepository


class GetDoctorUseCase:
    def __init__(
        self,
        doctor_repository: DoctorRepository,
        doctor_mapper: DoctorMapper,
    ) -> None:
        self.doctor_repository = doctor_repository
        self.doctor_mapper = doctor_mapper

    def handle(self, doctor_id: UUID) -> DetailedDoctorResponseDTO:
        user = self.doctor_repository.find_user_by_doctor_id(doctor_id)
        if user is None:
            raise DoctorNotFoundError
        return self.doctor_mapper.to_detailed_response(user)
