from typing import Annotated

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, model_validator
from pydantic_core import PydanticCustomError

from app.enums.models.hospitalization_action_sbar_clinical_course_enums import (
    HospitalizationActionSbarClinicalCourse,
)
from app.enums.models.hospitalization_action_sbar_priority_enums import (
    HospitalizationActionSbarPriority,
)
from app.enums.models.hospitalization_action_type_enums import HospitalizationActionType


class UpdateHospitalizationAction(BaseModel):
    description: str
    action_type: HospitalizationActionType
    files: list[UploadFile] | None
    sbar_situation: str | None
    sbar_background: str | None
    sbar_assessment: str | None
    sbar_recommendation: str | None
    sbar_plan: str | None
    sbar_priority: HospitalizationActionSbarPriority | None
    sbar_clinical_course: HospitalizationActionSbarClinicalCourse | None
    sbar_pending_items: str | None
    sbar_alerts: str | None
    sbar_source_transcript: str | None
    sbar_ai_generated: bool
    sbar_ai_review_confirmed: bool
    sbar_ai_warnings: str | None
    sbar_ai_missing_information: str | None
    sbar_ai_confidence: str | None

    def __init__(
        self,
        description: Annotated[
            str,
            Form(
                min_length=1,
                examples=["Observado que o paciente teve uma melhora nas últimas 24hr"],
            ),
        ],
        action_type: Annotated[
            HospitalizationActionType,
            Form(
                examples=[HospitalizationActionType.HOSPITALIZATION_VISIT],
            ),
        ] = HospitalizationActionType.HOSPITALIZATION_VISIT,
        files: Annotated[
            list[UploadFile] | None,
            File(description="Arquivos do hospitalização action"),
        ] = None,
        sbar_situation: Annotated[
            str | None,
            Form(min_length=1, examples=["Paciente estável nas últimas 24h"]),
        ] = None,
        sbar_background: Annotated[
            str | None,
            Form(examples=["Internado por pneumonia, DPOC prévio"]),
        ] = None,
        sbar_assessment: Annotated[
            str | None,
            Form(min_length=1, examples=["Evolução clínica estável"]),
        ] = None,
        sbar_recommendation: Annotated[
            str | None,
            Form(min_length=1, examples=["Manter conduta e revisar exames"]),
        ] = None,
        sbar_plan: Annotated[
            str | None,
            Form(examples=["Reavaliar amanhã após resultado dos exames"]),
        ] = None,
        sbar_priority: Annotated[
            HospitalizationActionSbarPriority | None,
            Form(examples=[HospitalizationActionSbarPriority.ATTENTION]),
        ] = None,
        sbar_clinical_course: Annotated[
            HospitalizationActionSbarClinicalCourse | None,
            Form(examples=[HospitalizationActionSbarClinicalCourse.STABLE]),
        ] = None,
        sbar_pending_items: Annotated[
            str | None,
            Form(examples=["Aguardar cultura"]),
        ] = None,
        sbar_alerts: Annotated[
            str | None,
            Form(examples=["Avisar se saturação abaixo de 92%"]),
        ] = None,
        sbar_source_transcript: Annotated[
            str | None,
            Form(examples=["paciente sem febre nega dor manter antibiótico"]),
        ] = None,
        sbar_ai_generated: Annotated[
            bool,
            Form(examples=[True]),
        ] = False,
        sbar_ai_review_confirmed: Annotated[
            bool,
            Form(examples=[True]),
        ] = False,
        sbar_ai_warnings: Annotated[
            str | None,
            Form(examples=['["Revise a conduta antes de salvar."]']),
        ] = None,
        sbar_ai_missing_information: Annotated[
            str | None,
            Form(examples=['["Sinais vitais completos."]']),
        ] = None,
        sbar_ai_confidence: Annotated[
            str | None,
            Form(
                examples=[
                    '{"situation":0.9,"background":0,"assessment":0.8,"recommendation":0.7,"plan":0.7}'
                ]
            ),
        ] = None,
    ) -> None:
        super().__init__(
            description=description,
            action_type=action_type,
            files=files,
            sbar_situation=sbar_situation,
            sbar_background=sbar_background,
            sbar_assessment=sbar_assessment,
            sbar_recommendation=sbar_recommendation,
            sbar_plan=sbar_plan,
            sbar_priority=sbar_priority,
            sbar_clinical_course=sbar_clinical_course,
            sbar_pending_items=sbar_pending_items,
            sbar_alerts=sbar_alerts,
            sbar_source_transcript=sbar_source_transcript,
            sbar_ai_generated=sbar_ai_generated,
            sbar_ai_review_confirmed=sbar_ai_review_confirmed,
            sbar_ai_warnings=sbar_ai_warnings,
            sbar_ai_missing_information=sbar_ai_missing_information,
            sbar_ai_confidence=sbar_ai_confidence,
        )

    def has_sbar_payload(self) -> bool:
        return any(
            [
                self.sbar_situation,
                self.sbar_background,
                self.sbar_assessment,
                self.sbar_recommendation,
                self.sbar_plan,
                self.sbar_priority,
                self.sbar_clinical_course,
                self.sbar_pending_items,
                self.sbar_alerts,
                self.sbar_source_transcript,
            ]
        )

    @model_validator(mode="after")
    def validate_sbar_required_fields(self) -> "UpdateHospitalizationAction":
        if not self.has_sbar_payload():
            return self
        required_fields = {
            "sbar_situation": self.sbar_situation,
            "sbar_assessment": self.sbar_assessment,
            "sbar_recommendation": self.sbar_recommendation,
            "sbar_priority": self.sbar_priority,
        }
        missing_fields = [
            field for field, value in required_fields.items() if not value
        ]
        if missing_fields:
            error_type = "sbar_required_fields"
            message = f"Campos SBAR obrigatórios ausentes: {', '.join(missing_fields)}"
            raise PydanticCustomError(error_type, message)
        return self
