from typing import Annotated
from uuid import UUID

from fastapi import Depends, Query, status
from fastapi.responses import JSONResponse

from app.modules.patients.di.use_cases import (
    get_create_patient_use_case,
    get_get_patient_use_case,
    get_paginate_patients_use_case,
    get_update_patient_use_case,
)
from app.modules.patients.dtos.patient.create_patient_dto import CreatePatientDTO
from app.modules.patients.dtos.patient.paginate_patients_dto import PaginatePatientsDTO
from app.modules.patients.dtos.patient.update_patient_dto import UpdatePatientDTO
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


def create_patient(
    data: CreatePatientDTO,
    create_patient_use_case: Annotated[
        CreatePatientUseCase, Depends(get_create_patient_use_case)
    ],
) -> JSONResponse:
    patient_response = create_patient_use_case.handle(data)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=patient_response.to_json(),
    )


def get_patient(
    patient_id: UUID,
    get_patient_use_case: Annotated[
        GetPatientUseCase, Depends(get_get_patient_use_case)
    ],
) -> JSONResponse:
    patient_response = get_patient_use_case.handle(patient_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=patient_response.to_json(),
    )


def update_patient(
    patient_id: UUID,
    data: UpdatePatientDTO,
    update_patient_use_case: Annotated[
        UpdatePatientUseCase, Depends(get_update_patient_use_case)
    ],
) -> JSONResponse:
    patient_response = update_patient_use_case.handle(patient_id, data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=patient_response.to_json(),
    )


def paginate_patients(
    params: Annotated[PaginatePatientsDTO, Query()],
    paginate_patients_use_case: Annotated[
        PaginatePatientsUseCase, Depends(get_paginate_patients_use_case)
    ],
) -> JSONResponse:
    return paginate_patients_use_case.handle(params)
