from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.hospitalization import Hospitalization


class Patient(SQLModel, table=True):
    __tablename__ = "patients"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(nullable=False)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    document_number: str | None = Field(default=None, nullable=True, unique=True)
    birth_date: date = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    hospitalizations: list["Hospitalization"] = Relationship(back_populates="patient")
