from uuid import UUID

from app.modules.doctor.dtos.doctor.update_doctor_dto import UpdateDoctorDTO
from app.modules.doctor.dtos.responses.doctor.detailed_doctor_response import (
    DetailedDoctorResponseDTO,
)
from app.modules.doctor.exceptions.doctor_already_exists_error import (
    DoctorAlreadyExistsError,
)
from app.modules.doctor.exceptions.doctor_not_found_error import DoctorNotFoundError
from app.modules.doctor.mappers.doctor_mapper import DoctorMapper
from app.modules.doctor.repositories.doctor_repository import DoctorRepository


class UpdateDoctorUseCase:
    def __init__(
        self,
        doctor_repository: DoctorRepository,
        doctor_mapper: DoctorMapper,
    ) -> None:
        self.doctor_repository = doctor_repository
        self.doctor_mapper = doctor_mapper

    def handle(
        self, doctor_id: UUID, data: UpdateDoctorDTO
    ) -> DetailedDoctorResponseDTO:
        user = self.doctor_repository.find_user_by_doctor_id(doctor_id)
        if user is None:
            raise DoctorNotFoundError

        self._validate_uniqueness(doctor_id, data)
        user = self.doctor_mapper.update_entity(user, data)
        user = self.doctor_repository.save_user(user)

        return self.doctor_mapper.to_detailed_response(user)

    def _validate_uniqueness(self, doctor_id: UUID, data: UpdateDoctorDTO) -> None:
        existing_email_user = self.doctor_repository.find_user_by_email(str(data.email))
        if existing_email_user is not None and existing_email_user.id != doctor_id:
            raise DoctorAlreadyExistsError.for_email()

        existing_document_user = self.doctor_repository.find_user_by_document(
            data.document
        )
        if (
            existing_document_user is not None
            and existing_document_user.id != doctor_id
        ):
            raise DoctorAlreadyExistsError.for_document()

        existing_crm_user = self.doctor_repository.find_user_by_crm(
            data.crm_uf,
            data.crm_number,
        )
        if existing_crm_user is not None and existing_crm_user.id != doctor_id:
            raise DoctorAlreadyExistsError.for_crm()
