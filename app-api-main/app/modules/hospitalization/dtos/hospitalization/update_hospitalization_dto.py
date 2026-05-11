from uuid import UUID

from pydantic import BaseModel, Field


class UpdateHospitalizationDTO(BaseModel):
    medical_team_id: UUID = Field(description="ID do time médico")
    number: str | None = Field(
        default=None, description="Número da internação", examples=["4659"]
    )
    place: str | None = Field(
        default=None, description="Local da internação", examples=["Santa casa"]
    )
    sector: str | None = Field(
        default=None, description="Setor da internação", examples=["UTI"]
    )
    reason: str | None = Field(
        default=None, description="Motivo da internação", examples=["Cirurgia"]
    )
    observation: str | None = Field(
        default=None,
        description="Observação da internação",
        examples=["Cisto na vesícula"],
    )
