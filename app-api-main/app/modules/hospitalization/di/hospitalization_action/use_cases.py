from typing import Annotated

from fastapi import Depends

from app.modules.hospitalization.di.hospitalization.repositories import (
    get_hospitalization_repository,
)
from app.modules.hospitalization.di.hospitalization_action.mappers import (
    get_hospitalization_action_mapper,
)
from app.modules.hospitalization.di.hospitalization_action.repositories import (
    get_hospitalization_action_attachment_repository,
    get_hospitalization_action_repository,
    get_hospitalization_action_sbar_repository,
)
from app.modules.hospitalization.di.hospitalization_action_attachment.services import (
    get_save_hospitalization_attachment,
)
from app.modules.hospitalization.mappers.hospitalization_action_mapper import (
    HospitalizationActionMapper,
)
from app.modules.hospitalization.repositories.hospitalization_action_attachment_repository import (
    HospitalizationActionAttachmentRepository,
)
from app.modules.hospitalization.repositories.hospitalization_action_repository import (
    HospitalizationActionRepository,
)
from app.modules.hospitalization.repositories.hospitalization_action_sbar_repository import (
    HospitalizationActionSbarRepository,
)
from app.modules.hospitalization.repositories.hospitalization_repository import (
    HospitalizationRepository,
)
from app.modules.hospitalization.services.hospitalization_actions_attachment.save_hospitalization_attachment import (
    SaveHospitalizationAttachment,
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


def get_create_hospitalization_action_use_case(
    repository: Annotated[
        HospitalizationActionRepository, Depends(get_hospitalization_action_repository)
    ],
    attachment_repository: Annotated[
        HospitalizationActionAttachmentRepository,
        Depends(get_hospitalization_action_attachment_repository),
    ],
    sbar_repository: Annotated[
        HospitalizationActionSbarRepository,
        Depends(get_hospitalization_action_sbar_repository),
    ],
    hospitalization_repository: Annotated[
        HospitalizationRepository, Depends(get_hospitalization_repository)
    ],
    save_hospitalization_attachment: Annotated[
        SaveHospitalizationAttachment, Depends(get_save_hospitalization_attachment)
    ],
    mapper: Annotated[
        HospitalizationActionMapper, Depends(get_hospitalization_action_mapper)
    ],
) -> CreateHospitalizationActionUseCase:
    return CreateHospitalizationActionUseCase(
        repository,
        attachment_repository,
        sbar_repository,
        hospitalization_repository,
        save_hospitalization_attachment,
        mapper,
    )


def get_get_hospitalization_action_use_case(
    repository: Annotated[
        HospitalizationActionRepository, Depends(get_hospitalization_action_repository)
    ],
    sbar_repository: Annotated[
        HospitalizationActionSbarRepository,
        Depends(get_hospitalization_action_sbar_repository),
    ],
    mapper: Annotated[
        HospitalizationActionMapper, Depends(get_hospitalization_action_mapper)
    ],
) -> GetHospitalizationActionUseCase:
    return GetHospitalizationActionUseCase(repository, mapper)


def get_paginate_hospitalization_actions_use_case(
    repository: Annotated[
        HospitalizationActionRepository, Depends(get_hospitalization_action_repository)
    ],
    mapper: Annotated[
        HospitalizationActionMapper, Depends(get_hospitalization_action_mapper)
    ],
) -> PaginateHospitalizationActionsUseCase:
    return PaginateHospitalizationActionsUseCase(repository, mapper)


def get_update_hospitalization_action_use_case(
    repository: Annotated[
        HospitalizationActionRepository, Depends(get_hospitalization_action_repository)
    ],
    sbar_repository: Annotated[
        HospitalizationActionSbarRepository,
        Depends(get_hospitalization_action_sbar_repository),
    ],
    mapper: Annotated[
        HospitalizationActionMapper, Depends(get_hospitalization_action_mapper)
    ],
    save_hospitalization_attachment: Annotated[
        SaveHospitalizationAttachment, Depends(get_save_hospitalization_attachment)
    ],
) -> UpdateHospitalizationActionUseCase:
    return UpdateHospitalizationActionUseCase(
        repository, sbar_repository, mapper, save_hospitalization_attachment
    )
