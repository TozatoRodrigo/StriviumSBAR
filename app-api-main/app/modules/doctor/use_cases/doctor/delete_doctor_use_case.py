from uuid import UUID

from app.modules.doctor.exceptions.doctor_not_found_error import DoctorNotFoundError
from app.modules.doctor.repositories.doctor_repository import DoctorRepository


class DeleteDoctorUseCase:
    def __init__(self, doctor_repository: DoctorRepository) -> None:
        self.doctor_repository = doctor_repository

    def handle(self, doctor_id: UUID) -> None:
        tenant_user = self.doctor_repository.find_tenant_user_by_user_id(doctor_id)
        if tenant_user is None:
            raise DoctorNotFoundError
        self.doctor_repository.delete_tenant_user_by_user_id(doctor_id)
