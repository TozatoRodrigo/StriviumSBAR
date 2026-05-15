from secrets import token_urlsafe
from uuid import UUID

from fastapi_pagination import Page

from app.enums.models.tenant_user_member_type_enums import TenantUserMemberType
from app.models.tenant_user import TenantUser
from app.models.user import User
from app.modules.doctor.dtos.doctor.create_doctor_dto import CreateDoctorDTO
from app.modules.doctor.dtos.doctor.update_doctor_dto import UpdateDoctorDTO
from app.modules.doctor.dtos.responses.doctor.detailed_doctor_response import (
    DetailedDoctorResponseDTO,
)
from app.modules.doctor.dtos.responses.doctor.doctor_crm_response import (
    DoctorCrmResponseDTO,
)
from app.modules.doctor.dtos.responses.doctor.doctor_response import DoctorResponseDTO
from app.modules.doctor.dtos.responses.doctor.paginate_doctors_response import (
    PaginateDoctorsResponseDTO,
)
from app.modules.user.utils.bcrypt import hash_password


class DoctorMapper:
    def __init__(self, tenant_id: UUID) -> None:
        self.tenant_id = tenant_id

    @staticmethod
    def _split_full_name(full_name: str) -> tuple[str, str]:
        normalized = " ".join(full_name.split()).strip()
        parts = normalized.split(" ", 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else parts[0]
        return first_name, last_name

    def to_entity(self, data: CreateDoctorDTO) -> User:
        first_name, last_name = self._split_full_name(data.full_name)
        return User(
            first_name=first_name,
            last_name=last_name,
            crm_state=data.crm_uf,
            crm_number=data.crm_number,
            document=data.document,
            email=data.email,
            password=hash_password(token_urlsafe(24)),
            birth_date=data.birth_date,
            cellphone=data.cellphone,
            gender=data.gender,
            specialty=data.specialty,
        )

    @staticmethod
    def update_entity(user: User, data: UpdateDoctorDTO) -> User:
        first_name, last_name = DoctorMapper._split_full_name(data.full_name)
        user.first_name = first_name
        user.last_name = last_name
        user.crm_state = data.crm_uf
        user.crm_number = data.crm_number
        user.document = data.document
        user.email = data.email
        user.birth_date = data.birth_date
        user.cellphone = data.cellphone
        user.gender = data.gender
        user.specialty = data.specialty
        return user

    @staticmethod
    def to_tenant_user_entity(
        user_id: UUID, role_id: UUID, tenant_id: UUID
    ) -> TenantUser:
        return TenantUser(
            tenant_id=tenant_id,
            user_id=user_id,
            role_id=role_id,
            member_type=TenantUserMemberType.DOCTOR,
        )

    @staticmethod
    def to_response(user: User) -> DoctorResponseDTO:
        return DoctorResponseDTO(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            crm=DoctorCrmResponseDTO(
                uf=user.crm_state or "",
                number=user.crm_number or "",
            ),
        )

    @staticmethod
    def to_detailed_response(user: User) -> DetailedDoctorResponseDTO:
        return DetailedDoctorResponseDTO(
            id=user.id,
            full_name=f"{user.first_name} {user.last_name}".strip(),
            birth_date=user.birth_date,
            cellphone=user.cellphone or "",
            gender=user.gender or "",
            document=user.document or "",
            email=user.email,
            specialty=user.specialty or "",
            crm_uf=user.crm_state or "",
            crm_number=user.crm_number or "",
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @staticmethod
    def to_paginate_response(
        pagination: Page[TenantUser],
    ) -> PaginateDoctorsResponseDTO:
        items = [DoctorMapper.to_response(item.user) for item in pagination.items]
        return PaginateDoctorsResponseDTO(
            data=items,
            total=pagination.total,
            page=pagination.page,
            limit=pagination.size,
            total_pages=pagination.pages,
        )
