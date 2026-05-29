from uuid import UUID

from fastapi import status

from app.enums.models.hospitalization_action_type_enums import HospitalizationActionType
from app.enums.models.hospitalization_status_enums import HospitalizationStatus
from app.exceptions.client_aware_error import ClientAwareError
from app.modules.hospitalization.dtos.hospitalization_action.create_hospitalization_action import (
    CreateHospitalizationAction,
)
from app.modules.hospitalization.dtos.responses.hospitalization_action.hospitalization_action_response import (
    HospitalizationActionResponse,
)
from app.modules.hospitalization.exceptions.hospitalization.hospitalization_not_found_error import (
    HospitalizationNotFoundError,
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

AI_REVIEW_REQUIRED_MESSAGE = "Rascunho SBAR gerado por IA exige revisão médica"
AI_SOURCE_TRANSCRIPT_REQUIRED_MESSAGE = (
    "Transcrição bruta é obrigatória para SBAR gerado por IA"
)
HOSPITALIZATION_NOT_ACTIVE_MESSAGE = (
    "Não é possível registrar evolução em uma internação encerrada"
)


class CreateHospitalizationActionUseCase:
    def __init__(
        self,
        hospitalization_action_repository: HospitalizationActionRepository,
        hospitalization_action_attachment_repository: HospitalizationActionAttachmentRepository,
        hospitalization_action_sbar_repository: HospitalizationActionSbarRepository,
        hospitalization_repository: HospitalizationRepository,
        save_hospitalization_attachment: SaveHospitalizationAttachment,
        mapper: HospitalizationActionMapper,
    ) -> None:
        self.hospitalization_action_repository = hospitalization_action_repository
        self.hospitalization_action_attachment_repository = (
            hospitalization_action_attachment_repository
        )
        self.hospitalization_action_sbar_repository = (
            hospitalization_action_sbar_repository
        )
        self.hospitalization_repository = hospitalization_repository
        self.save_hospitalization_attachment = save_hospitalization_attachment
        self.mapper = mapper

    def handle(
        self,
        hospitalization_action_data: CreateHospitalizationAction,
    ) -> HospitalizationActionResponse:
        self.__validate_ai_review(hospitalization_action_data)
        entity = self.mapper.to_entity(hospitalization_action_data)

        hospitalization = self.hospitalization_repository.get(entity.hospitalization_id)
        if hospitalization is None:
            raise HospitalizationNotFoundError(entity.hospitalization_id)
        self.__validate_hospitalization_is_active(hospitalization.status)

        hospitalization_action = self.hospitalization_action_repository.create(entity)
        if hospitalization_action.type in {
            HospitalizationActionType.HOSPITALIZATION_DISCHARGE,
            HospitalizationActionType.HOSPITALIZATION_DECEASED,
        }:
            self.__close_hospitalization(
                hospitalization_action.type, hospitalization_action.hospitalization_id
            )
        if hospitalization_action_data.files:
            self.save_hospitalization_attachment.save_files(
                hospitalization_action, hospitalization_action_data.files
            )
        if hospitalization_action_data.has_sbar_payload():
            self.hospitalization_action_sbar_repository.upsert(
                self.mapper.to_sbar_entity(
                    hospitalization_action.id, hospitalization_action_data
                )
            )
        hospitalization_action = self.hospitalization_action_repository.find_by_id(
            hospitalization_action.id
        )
        return self.mapper.to_response(hospitalization_action)

    def __close_hospitalization(
        self, status: HospitalizationActionType, hospitalization_id: UUID
    ) -> None:
        hospitalization = self.hospitalization_repository.get(hospitalization_id)
        if not hospitalization:
            return

        mapped_status = {
            HospitalizationActionType.HOSPITALIZATION_DISCHARGE: HospitalizationStatus.DISCHARGED,
            HospitalizationActionType.HOSPITALIZATION_DECEASED: HospitalizationStatus.DECEASED,
        }
        hospitalization.status = mapped_status[status]
        self.hospitalization_repository.save(hospitalization)

    @staticmethod
    def __validate_ai_review(data: CreateHospitalizationAction) -> None:
        if not data.sbar_ai_generated:
            return
        if not data.sbar_ai_review_confirmed:
            raise ClientAwareError(
                AI_REVIEW_REQUIRED_MESSAGE,
                status.HTTP_422_UNPROCESSABLE_CONTENT,
            )
        if not data.sbar_source_transcript:
            raise ClientAwareError(
                AI_SOURCE_TRANSCRIPT_REQUIRED_MESSAGE,
                status.HTTP_422_UNPROCESSABLE_CONTENT,
            )

    @staticmethod
    def __validate_hospitalization_is_active(
        hospitalization_status: HospitalizationStatus,
    ) -> None:
        if hospitalization_status == HospitalizationStatus.ACTIVE:
            return
        raise ClientAwareError(
            HOSPITALIZATION_NOT_ACTIVE_MESSAGE,
            status.HTTP_422_UNPROCESSABLE_CONTENT,
        )
