import json
from uuid import UUID

from fastapi_pagination import Page

from app.enums.models.hospitalization_action_status_enums import (
    HospitalizationActionStatus,
)
from app.exceptions.validation_error import ValidationError
from app.filesystem.filesystem import Filesystem
from app.models.hospitalization_action import HospitalizationAction
from app.models.hospitalization_action_sbar import HospitalizationActionSbar
from app.modules.hospitalization.dtos.hospitalization_action.create_hospitalization_action import (
    CreateHospitalizationAction,
)
from app.modules.hospitalization.dtos.hospitalization_action.update_hospitalization_action import (
    UpdateHospitalizationAction,
)
from app.modules.hospitalization.dtos.responses.hospitalization_action.hospitalization_action_media_response import (
    HospitalizationActionMediaResponse,
)
from app.modules.hospitalization.dtos.responses.hospitalization_action.hospitalization_action_response import (
    HospitalizationActionResponse,
)
from app.modules.hospitalization.dtos.responses.hospitalization_action.hospitalization_action_sbar_response import (
    HospitalizationActionSbarResponse,
)
from app.modules.hospitalization.dtos.responses.hospitalization_action.hospitalization_action_user_response import (
    HospitalizationActionUserResponse,
)
from app.modules.hospitalization.dtos.responses.hospitalization_action.paginate_hospitalization_action_response import (
    PaginateHospitalizationActionResponse,
)


class HospitalizationActionMapper:
    def __init__(
        self,
        tenant_id: UUID,
        user_id: UUID,
        hospitalization_id: UUID,
    ) -> None:
        self.tenant_id = tenant_id
        self.hospitalization_id = hospitalization_id
        self.user_id = user_id

    def to_entity(
        self,
        hospitalization_action_data: CreateHospitalizationAction,
    ) -> HospitalizationAction:
        return HospitalizationAction(
            tenant_id=self.tenant_id,
            hospitalization_id=self.hospitalization_id,
            user_id=self.user_id,
            description=hospitalization_action_data.description,
            status=HospitalizationActionStatus.COMPLETED,
            type=hospitalization_action_data.action_type,
        )

    def to_sbar_entity(
        self,
        hospitalization_action_id: UUID,
        hospitalization_action_data: CreateHospitalizationAction
        | UpdateHospitalizationAction,
    ) -> HospitalizationActionSbar:
        return HospitalizationActionSbar(
            tenant_id=self.tenant_id,
            hospitalization_action_id=hospitalization_action_id,
            situation=hospitalization_action_data.sbar_situation or "",
            background=hospitalization_action_data.sbar_background,
            assessment=hospitalization_action_data.sbar_assessment or "",
            recommendation=hospitalization_action_data.sbar_recommendation or "",
            plan=hospitalization_action_data.sbar_plan,
            priority=hospitalization_action_data.sbar_priority,
            clinical_course=hospitalization_action_data.sbar_clinical_course,
            pending_items=hospitalization_action_data.sbar_pending_items,
            alerts=hospitalization_action_data.sbar_alerts,
            source_transcript=hospitalization_action_data.sbar_source_transcript,
            ai_generated=hospitalization_action_data.sbar_ai_generated,
            ai_review_confirmed=hospitalization_action_data.sbar_ai_review_confirmed,
            ai_warnings=HospitalizationActionMapper._parse_json_list(
                hospitalization_action_data.sbar_ai_warnings
            ),
            ai_missing_information=HospitalizationActionMapper._parse_json_list(
                hospitalization_action_data.sbar_ai_missing_information
            ),
            ai_confidence=HospitalizationActionMapper._parse_json_dict(
                hospitalization_action_data.sbar_ai_confidence
            ),
        )

    @staticmethod
    def to_response(
        hospitalization_action: HospitalizationAction,
    ) -> HospitalizationActionResponse:
        user = None
        if hospitalization_action.user:
            user = HospitalizationActionUserResponse(
                id=hospitalization_action.user.id,
                first_name=hospitalization_action.user.first_name,
                last_name=hospitalization_action.user.last_name,
                member_type=hospitalization_action.user.tenant_users[0].member_type,
            )
        medias = []
        filesystem = Filesystem()
        if hospitalization_action.hospitalization_action_attachments:
            medias = [
                HospitalizationActionMediaResponse(
                    id=media.id,
                    type=media.type,
                    file_name=media.file_name,
                    file_path=filesystem.signed_url(media.file_path),
                )
                for media in hospitalization_action.hospitalization_action_attachments
            ]

        sbar = None
        if hospitalization_action.sbar:
            sbar = HospitalizationActionSbarResponse(
                id=hospitalization_action.sbar.id,
                situation=hospitalization_action.sbar.situation,
                background=hospitalization_action.sbar.background,
                assessment=hospitalization_action.sbar.assessment,
                recommendation=hospitalization_action.sbar.recommendation,
                plan=hospitalization_action.sbar.plan,
                priority=hospitalization_action.sbar.priority,
                clinical_course=hospitalization_action.sbar.clinical_course,
                pending_items=hospitalization_action.sbar.pending_items,
                alerts=hospitalization_action.sbar.alerts,
                source_transcript=hospitalization_action.sbar.source_transcript,
                ai_generated=hospitalization_action.sbar.ai_generated,
                ai_review_confirmed=hospitalization_action.sbar.ai_review_confirmed,
                ai_warnings=hospitalization_action.sbar.ai_warnings,
                ai_missing_information=hospitalization_action.sbar.ai_missing_information,
                ai_confidence=hospitalization_action.sbar.ai_confidence,
                created_at=hospitalization_action.sbar.created_at,
                updated_at=hospitalization_action.sbar.updated_at,
            )

        return HospitalizationActionResponse(
            id=hospitalization_action.id,
            hospitalization_id=hospitalization_action.hospitalization_id,
            user_id=hospitalization_action.user_id,
            user=user,
            description=hospitalization_action.description,
            status=hospitalization_action.status,
            type=hospitalization_action.type,
            medias=medias,
            sbar=sbar,
            created_at=hospitalization_action.created_at,
            updated_at=hospitalization_action.updated_at,
        )

    @staticmethod
    def to_paginate_response(
        pagination: Page[HospitalizationAction],
    ) -> PaginateHospitalizationActionResponse:
        items = [
            HospitalizationActionMapper.to_response(hospitalization_action)
            for hospitalization_action in pagination.items
        ]
        return PaginateHospitalizationActionResponse(
            data=items,
            total=pagination.total,
            page=pagination.page,
            limit=pagination.size,
            total_pages=pagination.pages,
        )

    @staticmethod
    def _parse_json_list(value: str | None) -> list[str] | None:
        if not value:
            return None
        parsed = json.loads(value)
        if not isinstance(parsed, list):
            message = "Expected JSON list"
            raise ValidationError(message)
        return [str(item) for item in parsed]

    @staticmethod
    def _parse_json_dict(value: str | None) -> dict[str, float] | None:
        if not value:
            return None
        parsed = json.loads(value)
        if not isinstance(parsed, dict):
            message = "Expected JSON object"
            raise ValidationError(message)
        return {str(key): float(parsed[key]) for key in parsed}
