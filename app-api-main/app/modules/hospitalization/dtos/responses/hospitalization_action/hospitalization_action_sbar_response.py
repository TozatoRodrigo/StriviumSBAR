from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.concerns.base_model import BaseModel
from app.enums.models.hospitalization_action_sbar_clinical_course_enums import (
    HospitalizationActionSbarClinicalCourse,
)
from app.enums.models.hospitalization_action_sbar_priority_enums import (
    HospitalizationActionSbarPriority,
)


class HospitalizationActionSbarResponse(BaseModel):
    id: UUID = Field(title="Hospitalization Action SBAR ID")
    situation: str = Field(title="Current clinical situation")
    background: str | None = Field(title="Relevant clinical background", default=None)
    assessment: str = Field(title="Clinical assessment")
    recommendation: str = Field(title="Recommendation and care plan")
    plan: str | None = Field(title="Care plan", default=None)
    priority: HospitalizationActionSbarPriority = Field(title="Visit priority")
    clinical_course: HospitalizationActionSbarClinicalCourse | None = Field(
        title="Clinical course compared to previous visit", default=None
    )
    pending_items: str | None = Field(title="Pending items", default=None)
    alerts: str | None = Field(title="Alerts for the next physician", default=None)
    source_transcript: str | None = Field(title="Raw dictated transcript", default=None)
    ai_generated: bool = Field(title="Whether SBAR was filled by AI", default=False)
    ai_review_confirmed: bool = Field(
        title="Whether physician confirmed AI draft review", default=False
    )
    ai_warnings: list[str] | None = Field(title="AI warnings", default=None)
    ai_missing_information: list[str] | None = Field(
        title="AI missing information", default=None
    )
    ai_confidence: dict[str, float] | None = Field(
        title="AI confidence by field", default=None
    )
    created_at: datetime = Field(title="Creation date")
    updated_at: datetime = Field(title="Update date")
