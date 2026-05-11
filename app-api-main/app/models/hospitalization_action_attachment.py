from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from app.enums.models.hospitalization_action_attachment_type_enums import (
    HospitalizationActionAttachmentType,
)

if TYPE_CHECKING:
    from app.models.hospitalization_action import HospitalizationAction


class HospitalizationActionAttachment(SQLModel, table=True):
    __tablename__ = "hospitalization_action_attachments"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(nullable=False, foreign_key="tenants.id")
    hospitalization_action_id: UUID = Field(
        nullable=False, foreign_key="hospitalization_actions.id"
    )
    type: HospitalizationActionAttachmentType = Field(nullable=False)
    file_name: str = Field(nullable=False)
    file_path: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    hospitalization_action: "HospitalizationAction" = Relationship(
        back_populates="hospitalization_action_attachments"
    )
