from typing import Annotated
from uuid import UUID

from fastapi import Depends, Query, status
from fastapi.responses import JSONResponse

from app.modules.medical_team.di.use_cases import (
    get_create_medical_team_use_case,
    get_delete_medical_team_use_case,
    get_paginate_medical_team_use_case,
    get_show_medical_team_by_id_use_case,
    get_update_medical_team_use_case,
)
from app.modules.medical_team.dtos.medical_team.create_medical_team_dto import (
    CreateMedicalTeamDTO,
)
from app.modules.medical_team.dtos.medical_team.paginate_medical_teams_dto import (
    PaginateMedicalTeamsDTO,
)
from app.modules.medical_team.dtos.medical_team.update_medical_team_dto import (
    UpdateMedicalTeamDTO,
)
from app.modules.medical_team.use_cases.medical_team.create_medical_team_use_case import (
    CreateMedicalTeamUseCase,
)
from app.modules.medical_team.use_cases.medical_team.delete_medical_team_use_case import (
    DeleteMedicalTeamUseCase,
)
from app.modules.medical_team.use_cases.medical_team.paginate_medical_teams_use_case import (
    PaginateMedicalTeamsUseCase,
)
from app.modules.medical_team.use_cases.medical_team.show_medical_team_by_id_use_case import (
    ShowMedicalTeamByIdUseCase,
)
from app.modules.medical_team.use_cases.medical_team.update_medical_team_use_case import (
    UpdateMedicalTeamUseCase,
)


def paginate_medical_team(
    params: Annotated[PaginateMedicalTeamsDTO, Query()],
    paginate_medical_team_use_case: Annotated[
        PaginateMedicalTeamsUseCase, Depends(get_paginate_medical_team_use_case)
    ],
) -> JSONResponse:
    data = paginate_medical_team_use_case.handle(params)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=data.to_json(),
    )


def create_medical_team(
    medical_team_dto: CreateMedicalTeamDTO,
    create_medical_team_use_case: Annotated[
        CreateMedicalTeamUseCase, Depends(get_create_medical_team_use_case)
    ],
) -> JSONResponse:
    result = create_medical_team_use_case.handle(medical_team_dto)
    return JSONResponse(result.to_json(), status_code=status.HTTP_201_CREATED)


def update_medical_team(
    medical_team_id: UUID,
    data: UpdateMedicalTeamDTO,
    update_medical_team_use_case: Annotated[
        UpdateMedicalTeamUseCase, Depends(get_update_medical_team_use_case)
    ],
) -> JSONResponse:
    result = update_medical_team_use_case.handle(medical_team_id, data)
    return JSONResponse(result.to_json(), status_code=status.HTTP_200_OK)


def delete_medical_team(
    medical_team_id: UUID,
    delete_medical_team_use_case: Annotated[
        DeleteMedicalTeamUseCase, Depends(get_delete_medical_team_use_case)
    ],
) -> None:
    delete_medical_team_use_case.handle(medical_team_id)
    return JSONResponse(content=None, status_code=status.HTTP_204_NO_CONTENT)


def get_medical_team_by_id(
    medical_team_id: UUID,
    show_medical_team_by_id_use_case: Annotated[
        ShowMedicalTeamByIdUseCase, Depends(get_show_medical_team_by_id_use_case)
    ],
) -> JSONResponse:
    result = show_medical_team_by_id_use_case.handle(medical_team_id)
    return JSONResponse(result.to_json(), status_code=status.HTTP_200_OK)
