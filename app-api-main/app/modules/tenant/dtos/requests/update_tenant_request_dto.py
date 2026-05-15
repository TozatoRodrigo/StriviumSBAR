from pydantic import BaseModel, Field


class UpdateTenantRequestDTO(BaseModel):
    name: str = Field(
        description="Nome do tenant",
        min_length=1,
        examples=["Santa casa"],
    )
