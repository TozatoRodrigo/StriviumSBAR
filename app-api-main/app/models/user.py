from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.hospitalization import Hospitalization
    from app.models.hospitalization_action import HospitalizationAction
    from app.models.medical_team_user import MedicalTeamUser
    from app.models.tenant_user import TenantUser


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    crm_state: str | None = Field(nullable=True)
    crm_number: str | None = Field(nullable=True)
    document: str | None = Field(nullable=True, unique=True)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    birth_date: date = Field(nullable=False)
    cellphone: str | None = Field(nullable=True)
    gender: str | None = Field(nullable=True)
    specialty: str | None = Field(nullable=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    hospitalization_actions: list["HospitalizationAction"] = Relationship(
        back_populates="user"
    )
    hospitalizations: list["Hospitalization"] = Relationship(back_populates="user")
    medical_team_users: list["MedicalTeamUser"] = Relationship(back_populates="user")
    tenant_users: list["TenantUser"] = Relationship(back_populates="user")
