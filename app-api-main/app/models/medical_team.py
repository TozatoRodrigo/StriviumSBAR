from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from app.enums.models.medical_teams_enums import MedicalTeamStatus

if TYPE_CHECKING:
    from app.models.hospitalization import Hospitalization
    from app.models.medical_team_user import MedicalTeamUser


class MedicalTeam(SQLModel, table=True):
    __tablename__ = "medical_teams"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(nullable=False, foreign_key="tenants.id")
    name: str = Field(nullable=False)
    description: str = Field(nullable=True)
    status: MedicalTeamStatus = Field(nullable=False, default=MedicalTeamStatus.ACTIVE)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    hospitalizations: list["Hospitalization"] = Relationship(
        back_populates="medical_team"
    )
    medical_team_users: list["MedicalTeamUser"] = Relationship(
        back_populates="medical_team"
    )
