from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from app.enums.models.medical_team_users_enums import MedicalTeamUserStatus

if TYPE_CHECKING:
    from app.models.medical_team import MedicalTeam
    from app.models.user import User


class MedicalTeamUser(SQLModel, table=True):
    __tablename__ = "medical_team_users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(nullable=False, foreign_key="tenants.id")
    medical_team_id: UUID = Field(nullable=False, foreign_key="medical_teams.id")
    user_id: UUID = Field(nullable=False, foreign_key="users.id")
    status: MedicalTeamUserStatus = Field(
        nullable=False, default=MedicalTeamUserStatus.ACTIVE
    )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    medical_team: "MedicalTeam" = Relationship(back_populates="medical_team_users")
    user: "User" = Relationship(back_populates="medical_team_users")
