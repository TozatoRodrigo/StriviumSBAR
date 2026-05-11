from pydantic import BaseModel, Field


class PaginateMedicalTeamsDTO(BaseModel):
    page: int = Field(default=1, description="Page number")
    limit: int = Field(default=10, description="Number of items per page")
    search: str | None = Field(default=None, description="Search query")
