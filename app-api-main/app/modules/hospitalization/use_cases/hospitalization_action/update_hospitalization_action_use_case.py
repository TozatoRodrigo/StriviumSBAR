from uuid import UUID

from fastapi import status

from app.enums.models.hospitalization_action_type_enums import HospitalizationActionType
from app.exceptions.client_aware_error import ClientAwareError
from app.modules.hospitalization.dtos.hospitalization_action.update_hospitalization_action import (
    UpdateHospitalizationAction,
)
from app.modules.hospitalization.dtos.responses.hospitalization_action.hospitalization_action_response import (
    HospitalizationActionResponse,
)
from app.modules.hospitalization.exceptions.hospitalization_action.hospitalization_action_not_found_error import (
    HospitalizationActionNotFoundError,
)
from app.modules.hospitalization.mappers.hospitalization_action_mapper import (
    HospitalizationActionMapper,
)
from app.modules.hospitalization.repositories.hospitalization_action_repository import (
    HospitalizationActionRepository,
)
from app.modules.hospitalization.repositories.hospitalization_action_sbar_repository import (
    HospitalizationActionSbarRepository,
)
from app.modules.hospitalization.services.hospitalization_actions_attachment.save_hospitalization_attachment import (
    SaveHospitalizationAttachment,
)

AI_REVIEW_REQUIRED_MESSAGE = "Rascunho SBAR gerado por IA exige revisão médica"
AI_SOURCE_TRANSCRIPT_REQUIRED_MESSAGE = (
    "Transcrição bruta é obrigatória para SBAR gerado por IA"
)
ACTION_TYPE_UPDATE_NOT_ALLOWED_MESSAGE = (
    "Não é permitido alterar o desfecho da internação ao editar uma evolução"
)


class UpdateHospitalizationActionUseCase:
    def __init__(
        self,
        repository: HospitalizationActionRepository,
        hospitalization_action_sbar_repository: HospitalizationActionSbarRepository,
        mapper: HospitalizationActionMapper,
        save_hospitalization_attachment: SaveHospitalizationAttachment,
    ) -> None:
        self.repository = repository
        self.hospitalization_action_sbar_repository = (
            hospitalization_action_sbar_repository
        )
        self.mapper = mapper
        self.save_hospitalization_attachment = save_hospitalization_attachment

    def handle(
        self,
        hospitalization_id: UUID,
        hospitalization_action_id: UUID,
        data: UpdateHospitalizationAction,
    ) -> HospitalizationActionResponse:
        self.__validate_ai_review(data)
        hospitalization_action = self.repository.find_by_id(hospitalization_action_id)
        if (
            hospitalization_action is None
            or hospitalization_action.hospitalization_id != hospitalization_id
        ):
            raise HospitalizationActionNotFoundError(hospitalization_action_id)
        self.__validate_action_type_immutable(
            current_action_type=hospitalization_action.type,
            new_action_type=data.action_type,
        )

        hospitalization_action.description = data.description

        if data.files:
            self.save_hospitalization_attachment.save_files(
                hospitalization_action, data.files
            )

        self.repository.update(hospitalization_action)
        if data.has_sbar_payload():
            self.hospitalization_action_sbar_repository.upsert(
                self.mapper.to_sbar_entity(hospitalization_action.id, data)
            )

        updated_hospitalization_action = self.repository.find_by_id(
            hospitalization_action.id
        )
        return self.mapper.to_response(updated_hospitalization_action)

    @staticmethod
    def __validate_ai_review(data: UpdateHospitalizationAction) -> None:
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
    def __validate_action_type_immutable(
        current_action_type: HospitalizationActionType,
        new_action_type: HospitalizationActionType,
    ) -> None:
        if current_action_type == new_action_type:
            return
        raise ClientAwareError(
            ACTION_TYPE_UPDATE_NOT_ALLOWED_MESSAGE,
            status.HTTP_422_UNPROCESSABLE_CONTENT,
        )
