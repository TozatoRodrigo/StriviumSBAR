from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.modules.medical_team.di.mappers import get_medical_team_mapper
from app.modules.medical_team.di.repositories import get_medical_team_repository
from app.modules.medical_team.mappers.medical_team_mapper import MedicalTeamMapper
from app.modules.medical_team.repositories.medical_team_repository import (
    MedicalTeamRepository,
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
from app.services.tenant.tenant_service import get_tenant_id_from_token


def get_create_medical_team_use_case(
    medical_team_repository: Annotated[
        MedicalTeamRepository, Depends(get_medical_team_repository)
    ],
    medical_team_mapper: Annotated[MedicalTeamMapper, Depends(get_medical_team_mapper)],
) -> CreateMedicalTeamUseCase:
    return CreateMedicalTeamUseCase(medical_team_repository, medical_team_mapper)


def get_update_medical_team_use_case(
    medical_team_repository: Annotated[
        MedicalTeamRepository, Depends(get_medical_team_repository)
    ],
    medical_team_mapper: Annotated[MedicalTeamMapper, Depends(get_medical_team_mapper)],
) -> UpdateMedicalTeamUseCase:
    return UpdateMedicalTeamUseCase(medical_team_repository, medical_team_mapper)


def get_paginate_medical_team_use_case(
    medical_team_repository: Annotated[
        MedicalTeamRepository, Depends(get_medical_team_repository)
    ],
    medical_team_mapper: Annotated[MedicalTeamMapper, Depends(get_medical_team_mapper)],
) -> PaginateMedicalTeamsUseCase:
    return PaginateMedicalTeamsUseCase(medical_team_repository, medical_team_mapper)


def get_show_medical_team_by_id_use_case(
    medical_team_repository: Annotated[
        MedicalTeamRepository, Depends(get_medical_team_repository)
    ],
    medical_team_mapper: Annotated[MedicalTeamMapper, Depends(get_medical_team_mapper)],
    tenant_id: Annotated[UUID, Depends(get_tenant_id_from_token)],
) -> ShowMedicalTeamByIdUseCase:
    return ShowMedicalTeamByIdUseCase(
        medical_team_repository, medical_team_mapper, tenant_id
    )


def get_delete_medical_team_use_case(
    medical_team_repository: Annotated[
        MedicalTeamRepository, Depends(get_medical_team_repository)
    ],
) -> DeleteMedicalTeamUseCase:
    return DeleteMedicalTeamUseCase(medical_team_repository)
