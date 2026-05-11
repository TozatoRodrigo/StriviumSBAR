from fastapi import UploadFile

from app.concerns.upload import Upload
from app.core.logging import logger
from app.enums.models.hospitalization_action_attachment_type_enums import (
    HospitalizationActionAttachmentType,
)
from app.models.hospitalization_action import HospitalizationAction
from app.models.hospitalization_action_attachment import HospitalizationActionAttachment
from app.modules.hospitalization.repositories.hospitalization_action_attachment_repository import (
    HospitalizationActionAttachmentRepository,
)


class SaveHospitalizationAttachment:
    def __init__(
        self,
        hospitalization_action_attachment_repository: HospitalizationActionAttachmentRepository,
        upload: Upload,
    ) -> None:
        self.hospitalization_action_attachment_repository = (
            hospitalization_action_attachment_repository
        )
        self.upload = upload

    def save_files(
        self,
        hospitalization_action: HospitalizationAction,
        files: list[UploadFile],
        throw_exception: bool = False,
    ) -> None:
        for file in files:
            try:
                self.save_file(hospitalization_action, file)
            except Exception as e:
                if throw_exception:
                    raise
                logger.warning(
                    f"Error saving file for hospitalization action {hospitalization_action.id} and file {file.filename}",
                    extra={"exception": str(e)},
                )

    def save_file(
        self, hospitalization_action: HospitalizationAction, file: UploadFile
    ) -> None:
        path = self.upload.upload(
            f"{hospitalization_action.tenant_id}/hospitalization_actions_attachments",
            file,
        )
        attachment = HospitalizationActionAttachment(
            tenant_id=hospitalization_action.tenant_id,
            hospitalization_action_id=hospitalization_action.id,
            type=self.__get_file_type(file),
            file_name=file.filename,
            file_path=path,
        )
        self.hospitalization_action_attachment_repository.save(attachment)

    @staticmethod
    def __get_file_type(file: UploadFile) -> HospitalizationActionAttachmentType:
        if file.content_type.startswith("image/"):
            return HospitalizationActionAttachmentType.PHOTO
        if file.content_type.startswith("video/"):
            return HospitalizationActionAttachmentType.VIDEO
        if file.content_type.startswith("audio/"):
            return HospitalizationActionAttachmentType.AUDIO
        return HospitalizationActionAttachmentType.DOCUMENT
