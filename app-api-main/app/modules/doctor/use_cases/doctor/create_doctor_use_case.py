from fastapi import status

from app.exceptions.client_aware_error import ClientAwareError
from app.modules.doctor.dtos.doctor.create_doctor_dto import CreateDoctorDTO
from app.modules.doctor.dtos.responses.doctor.detailed_doctor_response import (
    DetailedDoctorResponseDTO,
)
from app.modules.doctor.exceptions.doctor_already_exists_error import (
    DoctorAlreadyExistsError,
)
from app.modules.doctor.mappers.doctor_mapper import DoctorMapper
from app.modules.doctor.repositories.doctor_repository import DoctorRepository
from app.modules.doctor.repositories.role_repository import RoleRepository

DOCTOR_ROLE_NOT_FOUND_MESSAGE = "Papel de médico não encontrado"


class CreateDoctorUseCase:
    def __init__(
        self,
        doctor_repository: DoctorRepository,
        doctor_mapper: DoctorMapper,
        role_repository: RoleRepository,
    ) -> None:
        self.doctor_repository = doctor_repository
        self.doctor_mapper = doctor_mapper
        self.role_repository = role_repository

    def handle(self, data: CreateDoctorDTO) -> DetailedDoctorResponseDTO:
        self._validate_uniqueness(data)

        role = self.role_repository.get_doctor_role()
        if role is None:
            message = DOCTOR_ROLE_NOT_FOUND_MESSAGE
            raise ClientAwareError(
                message,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        user = self.doctor_mapper.to_entity(data)
        user = self.doctor_repository.save_user(user)

        tenant_user = self.doctor_mapper.to_tenant_user_entity(
            user_id=user.id,
            role_id=role.id,
            tenant_id=self.doctor_mapper.tenant_id,
        )
        self.doctor_repository.save_tenant_user(tenant_user)

        return self.doctor_mapper.to_detailed_response(user)

    def _validate_uniqueness(self, data: CreateDoctorDTO) -> None:
        existing_email_user = self.doctor_repository.find_user_by_email(str(data.email))
        if existing_email_user is not None:
            raise DoctorAlreadyExistsError.for_email()

        existing_document_user = self.doctor_repository.find_user_by_document(
            data.document
        )
        if existing_document_user is not None:
            raise DoctorAlreadyExistsError.for_document()

        existing_crm_user = self.doctor_repository.find_user_by_crm(
            data.crm_uf,
            data.crm_number,
        )
        if existing_crm_user is not None:
            raise DoctorAlreadyExistsError.for_crm()
