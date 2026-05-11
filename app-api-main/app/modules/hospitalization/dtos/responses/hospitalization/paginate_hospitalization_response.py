from pydantic import Field

from app.concerns.base_model import BaseModel

from .hospitalization_response import (
    HospitalizationResponse,
)


class PaginateHospitalizationResponse(BaseModel):
    data: list[HospitalizationResponse] = Field(description="Lista de internações")
    total: int = Field(description="Total de internações", examples=[20])
    page: int = Field(description="Página atual", examples=[1])
    limit: int = Field(description="Limite de internações", examples=[10])
    total_pages: int = Field(description="Total de páginas", examples=[2])
