from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.concerns.base_model import BaseModel
from app.enums.models.hospitalization_action_status_enums import (
    HospitalizationActionStatus,
)
from app.enums.models.hospitalization_action_type_enums import (
    HospitalizationActionType,
)

from .hospitalization_action_media_response import HospitalizationActionMediaResponse
from .hospitalization_action_sbar_response import HospitalizationActionSbarResponse
from .hospitalization_action_user_response import HospitalizationActionUserResponse


class HospitalizationActionResponse(BaseModel):
    id: UUID = Field(title="Hospitalization Action ID")
    hospitalization_id: UUID = Field(title="Hospitalization ID")
    user_id: UUID | None = Field(title="User ID")
    description: str = Field(
        title="Description of the hospitalization action",
        examples=["Observado que o paciente teve uma melhora nas últimas 24hr"],
    )
    status: HospitalizationActionStatus = Field(
        title="Status of the hospitalization action"
    )
    type: HospitalizationActionType = Field(title="Type of the hospitalization action")
    created_at: datetime = Field(title="Creation date of the hospitalization action")
    updated_at: datetime = Field(title="Update date of the hospitalization action")

    user: HospitalizationActionUserResponse | None = Field(
        title="User of the hospitalization action", default=None
    )
    medias: list[HospitalizationActionMediaResponse] = Field(
        title="Medias of the hospitalization action", default=[]
    )
    sbar: HospitalizationActionSbarResponse | None = Field(
        title="SBAR data of the hospitalization action", default=None
    )
