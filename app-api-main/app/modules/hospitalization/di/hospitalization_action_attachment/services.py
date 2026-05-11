from typing import Annotated

from fastapi import Depends

from app.concerns.upload import Upload
from app.di.concerns import get_upload
from app.modules.hospitalization.di.hospitalization_action_attachment.repositories import (
    get_hospitalization_action_attachment_repository,
)
from app.modules.hospitalization.repositories.hospitalization_action_attachment_repository import (
    HospitalizationActionAttachmentRepository,
)
from app.modules.hospitalization.services.hospitalization_actions_attachment.save_hospitalization_attachment import (
    SaveHospitalizationAttachment,
)


def get_save_hospitalization_attachment(
    hospitalization_action_attachment_repository: Annotated[
        HospitalizationActionAttachmentRepository,
        Depends(get_hospitalization_action_attachment_repository),
    ],
    upload: Annotated[Upload, Depends(get_upload)],
) -> SaveHospitalizationAttachment:
    return SaveHospitalizationAttachment(
        hospitalization_action_attachment_repository, upload
    )
