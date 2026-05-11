from pydantic import BaseModel, Field


class PaginateHospitalizationActionsDto(BaseModel):
    page: int = Field(default=1, ge=1, description="Página", examples=[1])
    limit: int = Field(default=10, ge=1, description="Limite", examples=[10])
