from typing import Annotated

from fastapi import Depends

from app.modules.hospitalization.di.hospitalization.mappers import (
    get_hospitalization_mapper,
)
from app.modules.hospitalization.di.hospitalization.repositories import (
    get_hospitalization_repository,
)
from app.modules.hospitalization.di.hospitalization.validations import (
    get_create_hospitalization_validations,
)
from app.modules.hospitalization.di.hospitalization_action.repositories import (
    get_hospitalization_action_repository,
)
from app.modules.hospitalization.mappers.hospitalization_mapper import (
    HospitalizationMapper,
)
from app.modules.hospitalization.repositories.hospitalization_action_repository import (
    HospitalizationActionRepository,
)
from app.modules.hospitalization.repositories.hospitalization_repository import (
    HospitalizationRepository,
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
from app.modules.hospitalization.validations.create_hospitalization.base_validation import (
    BaseValidation,
)


def get_create_hospitalization_use_case(
    hospitalization_repository: Annotated[
        HospitalizationRepository, Depends(get_hospitalization_repository)
    ],
    hospitalization_mapper: Annotated[
        HospitalizationMapper, Depends(get_hospitalization_mapper)
    ],
    hospitalization_action_repository: Annotated[
        HospitalizationActionRepository, Depends(get_hospitalization_action_repository)
    ],
    validations: Annotated[
        list[BaseValidation], Depends(get_create_hospitalization_validations)
    ],
) -> CreateHospitalizationUseCase:
    return CreateHospitalizationUseCase(
        repository=hospitalization_repository,
        mapper=hospitalization_mapper,
        hospitalization_action_repository=hospitalization_action_repository,
        validations=validations,
    )


def get_get_hospitalization_use_case(
    hospitalization_repository: Annotated[
        HospitalizationRepository, Depends(get_hospitalization_repository)
    ],
    hospitalization_mapper: Annotated[
        HospitalizationMapper, Depends(get_hospitalization_mapper)
    ],
) -> GetHospitalizationUseCase:
    return GetHospitalizationUseCase(
        repository=hospitalization_repository, mapper=hospitalization_mapper
    )


def get_paginate_hospitalizations_use_case(
    hospitalization_repository: Annotated[
        HospitalizationRepository, Depends(get_hospitalization_repository)
    ],
    hospitalization_mapper: Annotated[
        HospitalizationMapper, Depends(get_hospitalization_mapper)
    ],
) -> PaginateHospitalizationsUseCase:
    return PaginateHospitalizationsUseCase(
        repository=hospitalization_repository, mapper=hospitalization_mapper
    )


def get_paginate_pendings_hospitalizations_use_case(
    hospitalization_repository: Annotated[
        HospitalizationRepository, Depends(get_hospitalization_repository)
    ],
    hospitalization_mapper: Annotated[
        HospitalizationMapper, Depends(get_hospitalization_mapper)
    ],
) -> PaginatePendingsHospitalizationsUseCase:
    return PaginatePendingsHospitalizationsUseCase(
        repository=hospitalization_repository, mapper=hospitalization_mapper
    )


def get_paginate_completed_hospitalizations_use_case(
    hospitalization_repository: Annotated[
        HospitalizationRepository, Depends(get_hospitalization_repository)
    ],
    hospitalization_mapper: Annotated[
        HospitalizationMapper, Depends(get_hospitalization_mapper)
    ],
) -> PaginateCompletedHospitalizationsUseCase:
    return PaginateCompletedHospitalizationsUseCase(
        repository=hospitalization_repository, mapper=hospitalization_mapper
    )


def get_update_hospitalization_use_case(
    hospitalization_repository: Annotated[
        HospitalizationRepository, Depends(get_hospitalization_repository)
    ],
    hospitalization_mapper: Annotated[
        HospitalizationMapper, Depends(get_hospitalization_mapper)
    ],
) -> UpdateHospitalizationUseCase:
    return UpdateHospitalizationUseCase(
        repository=hospitalization_repository, mapper=hospitalization_mapper
    )
