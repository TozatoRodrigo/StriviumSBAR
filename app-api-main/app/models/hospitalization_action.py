from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from app.enums.models.hospitalization_action_status_enums import (
    HospitalizationActionStatus,
)
from app.enums.models.hospitalization_action_type_enums import HospitalizationActionType

if TYPE_CHECKING:
    from app.models.hospitalization import Hospitalization
    from app.models.hospitalization_action_attachment import (
        HospitalizationActionAttachment,
    )
    from app.models.hospitalization_action_sbar import HospitalizationActionSbar
    from app.models.user import User


class HospitalizationAction(SQLModel, table=True):
    __tablename__ = "hospitalization_actions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(nullable=False)
    hospitalization_id: UUID = Field(nullable=False, foreign_key="hospitalizations.id")
    user_id: UUID | None = Field(nullable=True, foreign_key="users.id")
    status: HospitalizationActionStatus = Field(nullable=False)
    type: HospitalizationActionType = Field(nullable=False)
    description: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    user: Optional["User"] = Relationship(back_populates="hospitalization_actions")
    hospitalization: "Hospitalization" = Relationship(
        back_populates="hospitalization_actions"
    )
    hospitalization_action_attachments: list["HospitalizationActionAttachment"] = (
        Relationship(back_populates="hospitalization_action")
    )
    sbar: Optional["HospitalizationActionSbar"] = Relationship(
        back_populates="hospitalization_action",
        sa_relationship_kwargs={"uselist": False},
    )
