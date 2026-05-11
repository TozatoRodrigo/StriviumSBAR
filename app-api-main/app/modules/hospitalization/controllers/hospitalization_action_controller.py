from typing import Annotated
from uuid import UUID

from fastapi import Depends, Path, Query, status
from fastapi.responses import JSONResponse

from app.modules.hospitalization.di.hospitalization_action.use_cases import (
    get_create_hospitalization_action_use_case,
    get_get_hospitalization_action_use_case,
    get_paginate_hospitalization_actions_use_case,
    get_update_hospitalization_action_use_case,
)
from app.modules.hospitalization.dtos.hospitalization_action.create_hospitalization_action import (
    CreateHospitalizationAction,
)
from app.modules.hospitalization.dtos.hospitalization_action.paginate_hospitalization_actions_dto import (
    PaginateHospitalizationActionsDto,
)
from app.modules.hospitalization.dtos.hospitalization_action.update_hospitalization_action import (
    UpdateHospitalizationAction,
)
from app.modules.hospitalization.use_cases.hospitalization_action.create_hospitalization_action_use_case import (
    CreateHospitalizationActionUseCase,
)
from app.modules.hospitalization.use_cases.hospitalization_action.get_hospitalization_action_use_case import (
    GetHospitalizationActionUseCase,
)
from app.modules.hospitalization.use_cases.hospitalization_action.paginate_hospitalization_actions_use_case import (
    PaginateHospitalizationActionsUseCase,
)
from app.modules.hospitalization.use_cases.hospitalization_action.update_hospitalization_action_use_case import (
    UpdateHospitalizationActionUseCase,
)


def create_hospitalization_action(
    hospitalization_action_data: Annotated[CreateHospitalizationAction, Depends()],
    create_hospitalization_action_use_case: Annotated[
        CreateHospitalizationActionUseCase,
        Depends(get_create_hospitalization_action_use_case),
    ],
) -> JSONResponse:
    hospitalization_action_response = create_hospitalization_action_use_case.handle(
        hospitalization_action_data
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=hospitalization_action_response.to_json(),
    )


def get_hospitalization_action(
    hospitalization_action_id: Annotated[UUID, Path(title="Hospitalization Action ID")],
    get_hospitalization_action_use_case: Annotated[
        GetHospitalizationActionUseCase,
        Depends(get_get_hospitalization_action_use_case),
    ],
) -> JSONResponse:
    hospitalization_action = get_hospitalization_action_use_case.handle(
        hospitalization_action_id
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=hospitalization_action.to_json(),
    )


def paginate_hospitalization_actions(
    hospitalization_id: Annotated[UUID, Path(title="Hospitalization ID")],
    paginate_hospitalization_actions_use_case: Annotated[
        PaginateHospitalizationActionsUseCase,
        Depends(get_paginate_hospitalization_actions_use_case),
    ],
    params: Annotated[PaginateHospitalizationActionsDto, Query()],
) -> JSONResponse:
    hospitalization_actions = paginate_hospitalization_actions_use_case.handle(
        hospitalization_id, params.page, params.limit
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=hospitalization_actions.to_json(),
    )


def update_hospitalization_action(
    hospitalization_action_id: Annotated[UUID, Path(title="Hospitalization Action ID")],
    data: Annotated[UpdateHospitalizationAction, Depends()],
    update_hospitalization_action_use_case: Annotated[
        UpdateHospitalizationActionUseCase,
        Depends(get_update_hospitalization_action_use_case),
    ],
) -> JSONResponse:
    result = update_hospitalization_action_use_case.handle(
        hospitalization_action_id, data
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=result.to_json(),
    )
