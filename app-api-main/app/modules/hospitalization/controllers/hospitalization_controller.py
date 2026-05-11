from typing import Annotated
from uuid import UUID

from fastapi import Depends, Query, status
from fastapi.responses import JSONResponse

from app.modules.hospitalization.di.hospitalization.use_cases import (
    get_create_hospitalization_use_case,
    get_get_hospitalization_use_case,
    get_paginate_completed_hospitalizations_use_case,
    get_paginate_hospitalizations_use_case,
    get_paginate_pendings_hospitalizations_use_case,
    get_update_hospitalization_use_case,
)
from app.modules.hospitalization.dtos.hospitalization.create_hospitalization_dto import (
    CreateHospitalizationDTO,
)
from app.modules.hospitalization.dtos.hospitalization.paginate_hospitalizations_dto import (
    PaginateHospitalizationsDTO,
)
from app.modules.hospitalization.dtos.hospitalization.update_hospitalization_dto import (
    UpdateHospitalizationDTO,
)
from app.modules.hospitalization.services.hospitalization.hospitalization_service import (
    get_hospitalization_id_from_path,
)
from app.modules.hospitalization.use_cases.hospitalization.create_hospitalization_use_case import (
    CreateHospitalizationUseCase,
)
from app.modules.hospitalization.use_cases.hospitalization.get_hospitalization_use_case import (
    GetHospitalizationUseCase,
)
from app.modules.hospitalization.use_cases.hospitalization.paginate_completed_hospitalizations_use_case import (
    PaginateCompletedHospitalizationsUseCase,
)
from app.modules.hospitalization.use_cases.hospitalization.paginate_hospitalizations_use_case import (
    PaginateHospitalizationsUseCase,
)
from app.modules.hospitalization.use_cases.hospitalization.paginate_pendings_hospitalizations_use_case import (
    PaginatePendingsHospitalizationsUseCase,
)
from app.modules.hospitalization.use_cases.hospitalization.update_hospitalization_use_case import (
    UpdateHospitalizationUseCase,
)


def create_hospitalization(
    data: CreateHospitalizationDTO,
    create_hospitalization_use_case: Annotated[
        CreateHospitalizationUseCase, Depends(get_create_hospitalization_use_case)
    ],
) -> JSONResponse:
    hospitalization_response = create_hospitalization_use_case.handle(data)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=hospitalization_response.to_json()
    )


def paginate_hospitalizations(
    paginate_hospitalizations_use_case: Annotated[
        PaginateHospitalizationsUseCase, Depends(get_paginate_hospitalizations_use_case)
    ],
    params: Annotated[PaginateHospitalizationsDTO, Query()],
) -> JSONResponse:
    hospitalizations_response = paginate_hospitalizations_use_case.handle(
        params.page, params.limit, params.patient_id, params.search
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=hospitalizations_response.to_json()
    )


def paginate_pendings_hospitalizations(
    paginate_pendings_hospitalizations_use_case: Annotated[
        PaginatePendingsHospitalizationsUseCase,
        Depends(get_paginate_pendings_hospitalizations_use_case),
    ],
    params: Annotated[PaginateHospitalizationsDTO, Query()],
) -> JSONResponse:
    hospitalizations_response = paginate_pendings_hospitalizations_use_case.handle(
        params.page, params.limit, params.search
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=hospitalizations_response.to_json()
    )


def paginate_completed_hospitalizations(
    paginate_completed_hospitalizations_use_case: Annotated[
        PaginateCompletedHospitalizationsUseCase,
        Depends(get_paginate_completed_hospitalizations_use_case),
    ],
    params: Annotated[PaginateHospitalizationsDTO, Query()],
) -> JSONResponse:
    hospitalizations_response = paginate_completed_hospitalizations_use_case.handle(
        params.page, params.limit
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=hospitalizations_response.to_json()
    )


def get_hospitalization(
    hospitalization_id: Annotated[UUID, Depends(get_hospitalization_id_from_path)],
    get_hospitalization_use_case: Annotated[
        GetHospitalizationUseCase, Depends(get_get_hospitalization_use_case)
    ],
) -> JSONResponse:
    hospitalization_response = get_hospitalization_use_case.handle(hospitalization_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=hospitalization_response.to_json()
    )


def update_hospitalization(
    hospitalization_id: Annotated[UUID, Depends(get_hospitalization_id_from_path)],
    data: UpdateHospitalizationDTO,
    update_hospitalization_use_case: Annotated[
        UpdateHospitalizationUseCase, Depends(get_update_hospitalization_use_case)
    ],
) -> JSONResponse:
    hospitalization_response = update_hospitalization_use_case.handle(
        hospitalization_id, data
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=hospitalization_response.to_json()
    )
