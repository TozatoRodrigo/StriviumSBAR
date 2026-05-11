from typing import Annotated

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, model_validator

from app.enums.models.hospitalization_action_sbar_clinical_course_enums import (
    HospitalizationActionSbarClinicalCourse,
)
from app.enums.models.hospitalization_action_sbar_priority_enums import (
    HospitalizationActionSbarPriority,
)
from app.enums.models.hospitalization_action_type_enums import HospitalizationActionType


class CreateHospitalizationAction(BaseModel):
    description: str
    action_type: HospitalizationActionType
    files: list[UploadFile] | None
    sbar_situation: str | None
    sbar_background: str | None
    sbar_assessment: str | None
    sbar_recommendation: str | None
    sbar_priority: HospitalizationActionSbarPriority | None
    sbar_clinical_course: HospitalizationActionSbarClinicalCourse | None
    sbar_pending_items: str | None
    sbar_alerts: str | None

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
    ) -> None:
        super().__init__(
            description=description,
            action_type=action_type,
            files=files,
            sbar_situation=sbar_situation,
            sbar_background=sbar_background,
            sbar_assessment=sbar_assessment,
            sbar_recommendation=sbar_recommendation,
            sbar_priority=sbar_priority,
            sbar_clinical_course=sbar_clinical_course,
            sbar_pending_items=sbar_pending_items,
            sbar_alerts=sbar_alerts,
        )

    def has_sbar_payload(self) -> bool:
        return any(
            [
                self.sbar_situation,
                self.sbar_background,
                self.sbar_assessment,
                self.sbar_recommendation,
                self.sbar_priority,
                self.sbar_clinical_course,
                self.sbar_pending_items,
                self.sbar_alerts,
            ]
        )

    @model_validator(mode="after")
    def validate_sbar_required_fields(self) -> "CreateHospitalizationAction":
        if not self.has_sbar_payload():
            return self
        required_fields = {
            "sbar_situation": self.sbar_situation,
            "sbar_assessment": self.sbar_assessment,
            "sbar_recommendation": self.sbar_recommendation,
            "sbar_priority": self.sbar_priority,
        }
        missing_fields = [field for field, value in required_fields.items() if not value]
        if missing_fields:
            raise ValueError(
                f"Campos SBAR obrigatórios ausentes: {', '.join(missing_fields)}"
            )
        return self
