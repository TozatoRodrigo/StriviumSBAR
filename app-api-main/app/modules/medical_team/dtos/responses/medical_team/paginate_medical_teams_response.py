from pydantic import Field

from app.concerns.base_model import BaseModel
from app.modules.medical_team.dtos.responses.medical_team.medical_team_response import (
    MedicalTeamResponse,
)


class PaginateMedicalTeamsResponse(BaseModel):
    data: list[MedicalTeamResponse] = Field(
        default=[], description="List of medical teams"
    )
    page: int = Field(default=1, description="Page number")
    limit: int = Field(default=10, description="Number of items per page")
    total: int = Field(default=0, description="Total number of items")
    total_pages: bool = Field(default=False, description="Has next page")
