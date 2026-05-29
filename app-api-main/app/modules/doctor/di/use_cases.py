from typing import Annotated

from fastapi import Depends

from app.modules.doctor.di.mappers import get_doctor_mapper
from app.modules.doctor.di.repositories import (
    get_doctor_repository,
    get_role_repository,
)
from app.modules.doctor.mappers.doctor_mapper import DoctorMapper
from app.modules.doctor.repositories.doctor_repository import DoctorRepository
from app.modules.doctor.repositories.role_repository import RoleRepository
from app.modules.doctor.use_cases.doctor.create_doctor_use_case import (
    CreateDoctorUseCase,
)
from app.modules.doctor.use_cases.doctor.delete_doctor_use_case import (
    DeleteDoctorUseCase,
)
from app.modules.doctor.use_cases.doctor.get_doctor_use_case import GetDoctorUseCase
from app.modules.doctor.use_cases.doctor.paginate_doctors_use_case import (
    PaginateDoctorsUseCase,
)
from app.modules.doctor.use_cases.doctor.update_doctor_use_case import (
    UpdateDoctorUseCase,
)


def get_create_doctor_use_case(
    doctor_repository: Annotated[DoctorRepository, Depends(get_doctor_repository)],
    doctor_mapper: Annotated[DoctorMapper, Depends(get_doctor_mapper)],
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
) -> CreateDoctorUseCase:
    return CreateDoctorUseCase(doctor_repository, doctor_mapper, role_repository)


def get_paginate_doctors_use_case(
    doctor_repository: Annotated[DoctorRepository, Depends(get_doctor_repository)],
    doctor_mapper: Annotated[DoctorMapper, Depends(get_doctor_mapper)],
) -> PaginateDoctorsUseCase:
    return PaginateDoctorsUseCase(doctor_repository, doctor_mapper)


def get_get_doctor_use_case(
    doctor_repository: Annotated[DoctorRepository, Depends(get_doctor_repository)],
    doctor_mapper: Annotated[DoctorMapper, Depends(get_doctor_mapper)],
) -> GetDoctorUseCase:
    return GetDoctorUseCase(doctor_repository, doctor_mapper)


def get_update_doctor_use_case(
    doctor_repository: Annotated[DoctorRepository, Depends(get_doctor_repository)],
    doctor_mapper: Annotated[DoctorMapper, Depends(get_doctor_mapper)],
) -> UpdateDoctorUseCase:
    return UpdateDoctorUseCase(doctor_repository, doctor_mapper)


def get_delete_doctor_use_case(
    doctor_repository: Annotated[DoctorRepository, Depends(get_doctor_repository)],
) -> DeleteDoctorUseCase:
    return DeleteDoctorUseCase(doctor_repository)
