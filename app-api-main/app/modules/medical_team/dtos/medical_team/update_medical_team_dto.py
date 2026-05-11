from pydantic import BaseModel, Field


class UpdateMedicalTeamDTO(BaseModel):
    name: str | None = Field(
        default=None,
        description="Nome do time médico",
        max_length=150,
        examples=["Emergências"],
    )
    description: str | None = Field(
        default=None,
        description="Descrição do time médico",
        max_length=255,
        examples=["Equipe focada em atendimento de emergências"],
    )
