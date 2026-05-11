from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, Text
from sqlmodel import Field, Relationship, SQLModel

from app.enums.models.hospitalization_action_sbar_clinical_course_enums import (
    HospitalizationActionSbarClinicalCourse,
)
from app.enums.models.hospitalization_action_sbar_priority_enums import (
    HospitalizationActionSbarPriority,
)

if TYPE_CHECKING:
    from app.models.hospitalization_action import HospitalizationAction


class HospitalizationActionSbar(SQLModel, table=True):
    __tablename__ = "hospitalization_action_sbars"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(nullable=False, foreign_key="tenants.id")
    hospitalization_action_id: UUID = Field(
        nullable=False,
        foreign_key="hospitalization_actions.id",
        sa_column_kwargs={"unique": True},
    )
    situation: str = Field(sa_column=Column(Text, nullable=False))
    background: str | None = Field(default=None, sa_column=Column(Text, nullable=True))
    assessment: str = Field(sa_column=Column(Text, nullable=False))
    recommendation: str = Field(sa_column=Column(Text, nullable=False))
    priority: HospitalizationActionSbarPriority = Field(nullable=False)
    clinical_course: HospitalizationActionSbarClinicalCourse | None = Field(
        default=None, nullable=True
    )
    pending_items: str | None = Field(default=None, sa_column=Column(Text, nullable=True))
    alerts: str | None = Field(default=None, sa_column=Column(Text, nullable=True))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    hospitalization_action: Optional["HospitalizationAction"] = Relationship(
        back_populates="sbar"
    )
