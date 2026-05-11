from pydantic import Field

from app.concerns.base_model import BaseModel

from .hospitalization_action_response import HospitalizationActionResponse


class PaginateHospitalizationActionResponse(BaseModel):
    data: list[HospitalizationActionResponse] = Field(
        description="Lista de ações de internação"
    )
    total: int = Field(description="Total de ações de internação", examples=[20])
    page: int = Field(description="Página atual", examples=[1])
    limit: int = Field(description="Limite de ações de internação", examples=[10])
    total_pages: int = Field(description="Total de páginas", examples=[2])
