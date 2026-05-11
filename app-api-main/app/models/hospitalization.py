from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from app.enums.models.hospitalization_status_enums import HospitalizationStatus

if TYPE_CHECKING:
    from app.models.hospitalization_action import HospitalizationAction
    from app.models.medical_team import MedicalTeam
    from app.models.patient import Patient
    from app.models.tenant import Tenant
    from app.models.user import User


class Hospitalization(SQLModel, table=True):
    __tablename__: str = "hospitalizations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(nullable=False, foreign_key="tenants.id")
    user_id: UUID = Field(nullable=False, foreign_key="users.id")
    patient_id: UUID = Field(nullable=False, foreign_key="patients.id")
    medical_team_id: UUID = Field(nullable=False, foreign_key="medical_teams.id")
    status: HospitalizationStatus = Field(nullable=False)
    hospitalization_number: str | None = Field(nullable=True)
    hospitalization_place: str | None = Field(nullable=True)
    hospitalization_sector: str | None = Field(nullable=True)
    hospitalization_reason: str | None = Field(nullable=True)
    observation: str | None = Field(nullable=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    tenant: "Tenant" = Relationship(back_populates="hospitalizations")
    user: "User" = Relationship(back_populates="hospitalizations")
    patient: "Patient" = Relationship(back_populates="hospitalizations")
    medical_team: "MedicalTeam" = Relationship(back_populates="hospitalizations")
    hospitalization_actions: list["HospitalizationAction"] = Relationship(
        back_populates="hospitalization"
    )
