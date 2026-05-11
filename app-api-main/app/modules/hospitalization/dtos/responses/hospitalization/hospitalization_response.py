from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.concerns.base_model import BaseModel
from app.enums.models.hospitalization_status_enums import HospitalizationStatus

from .patient_response import (
    PatientResponse,
)


class HospitalizationResponse(BaseModel):
    id: UUID = Field(description="ID da hospitalização")
    user_id: UUID = Field(description="ID do médico")
    patient_id: UUID = Field(description="ID do paciente")
    medical_team_id: UUID = Field(description="ID do time médico")
    status: HospitalizationStatus = Field(description="Status da hospitalização")
    number: str | None = Field(
        description="Número da hospitalização", examples=["123456"]
    )
    place: str | None = Field(
        description="Local da hospitalização", examples=["Sala 1"]
    )
    sector: str | None = Field(
        description="Setor da hospitalização", examples=["Cardiologia"]
    )
    reason: str | None = Field(
        description="Motivo da hospitalização", examples=["Paciente sofreu um AVC"]
    )
    observation: str | None = Field(
        description="Observação da hospitalização",
        examples=["Paciente alérgico a morfina"],
    )
    created_at: datetime = Field(description="Data de criação")
    updated_at: datetime = Field(description="Data de atualização")

    patient: PatientResponse = Field(description="Dados do paciente")
