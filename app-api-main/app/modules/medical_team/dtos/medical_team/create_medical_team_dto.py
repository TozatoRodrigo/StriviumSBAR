from pydantic import BaseModel, Field


class CreateMedicalTeamDTO(BaseModel):
    name: str = Field(
        description="Nome do time médico",
        max_length=150,
        examples=["Emergências"],
    )
    description: str = Field(
        description="Descrição do time médico",
        max_length=255,
        examples=["Equipe focada em atendimento de emergências"],
    )
