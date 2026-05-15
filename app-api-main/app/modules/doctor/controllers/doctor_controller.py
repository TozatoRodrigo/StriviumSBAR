from typing import Annotated
from uuid import UUID

from fastapi import Depends, Query, status
from fastapi.responses import JSONResponse

from app.modules.doctor.di.use_cases import (
    get_create_doctor_use_case,
    get_delete_doctor_use_case,
    get_get_doctor_use_case,
    get_paginate_doctors_use_case,
    get_update_doctor_use_case,
)
from app.modules.doctor.dtos.doctor.create_doctor_dto import CreateDoctorDTO
from app.modules.doctor.dtos.doctor.paginate_doctors_dto import PaginateDoctorsDTO
from app.modules.doctor.dtos.doctor.update_doctor_dto import UpdateDoctorDTO
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


def create_doctor(
    data: CreateDoctorDTO,
    create_doctor_use_case: Annotated[
        CreateDoctorUseCase, Depends(get_create_doctor_use_case)
    ],
) -> JSONResponse:
    result = create_doctor_use_case.handle(data)
    return JSONResponse(content=result.to_json(), status_code=status.HTTP_201_CREATED)


def paginate_doctors(
    params: Annotated[PaginateDoctorsDTO, Query()],
    paginate_doctors_use_case: Annotated[
        PaginateDoctorsUseCase, Depends(get_paginate_doctors_use_case)
    ],
) -> JSONResponse:
    result = paginate_doctors_use_case.handle(params)
    return JSONResponse(content=result.to_json(), status_code=status.HTTP_200_OK)


def get_doctor(
    doctor_id: UUID,
    get_doctor_use_case: Annotated[GetDoctorUseCase, Depends(get_get_doctor_use_case)],
) -> JSONResponse:
    result = get_doctor_use_case.handle(doctor_id)
    return JSONResponse(content=result.to_json(), status_code=status.HTTP_200_OK)


def update_doctor(
    doctor_id: UUID,
    data: UpdateDoctorDTO,
    update_doctor_use_case: Annotated[
        UpdateDoctorUseCase, Depends(get_update_doctor_use_case)
    ],
) -> JSONResponse:
    result = update_doctor_use_case.handle(doctor_id, data)
    return JSONResponse(content=result.to_json(), status_code=status.HTTP_200_OK)


def delete_doctor(
    doctor_id: UUID,
    delete_doctor_use_case: Annotated[
        DeleteDoctorUseCase, Depends(get_delete_doctor_use_case)
    ],
) -> JSONResponse:
    delete_doctor_use_case.handle(doctor_id)
    return JSONResponse(content=None, status_code=status.HTTP_204_NO_CONTENT)
