from typing import Annotated

from fastapi import Depends

from app.modules.patients.di.mappers import get_patient_mapper
from app.modules.patients.di.repositories import get_patient_repository
from app.modules.patients.mappers.patient_mapper import PatientMapper
from app.modules.patients.repositories.patient_repository import PatientRepository
from app.modules.patients.use_cases.patient.create_patient_use_case import (
    CreatePatientUseCase,
)
from app.modules.patients.use_cases.patient.get_patient_use_case import (
    GetPatientUseCase,
)
from app.modules.patients.use_cases.patient.paginate_patients_use_case import (
    PaginatePatientsUseCase,
)
from app.modules.patients.use_cases.patient.update_patient_use_case import (
    UpdatePatientUseCase,
)


def get_create_patient_use_case(
    patient_repository: Annotated[PatientRepository, Depends(get_patient_repository)],
    patient_mapper: Annotated[PatientMapper, Depends(get_patient_mapper)],
) -> CreatePatientUseCase:
    return CreatePatientUseCase(patient_repository, patient_mapper)


def get_paginate_patients_use_case(
    patient_repository: Annotated[PatientRepository, Depends(get_patient_repository)],
    patient_mapper: Annotated[PatientMapper, Depends(get_patient_mapper)],
) -> PaginatePatientsUseCase:
    return PaginatePatientsUseCase(patient_repository, patient_mapper)


def get_get_patient_use_case(
    patient_repository: Annotated[PatientRepository, Depends(get_patient_repository)],
    patient_mapper: Annotated[PatientMapper, Depends(get_patient_mapper)],
) -> GetPatientUseCase:
    return GetPatientUseCase(patient_repository, patient_mapper)


def get_update_patient_use_case(
    patient_repository: Annotated[PatientRepository, Depends(get_patient_repository)],
    patient_mapper: Annotated[PatientMapper, Depends(get_patient_mapper)],
) -> UpdatePatientUseCase:
    return UpdatePatientUseCase(patient_repository, patient_mapper)
