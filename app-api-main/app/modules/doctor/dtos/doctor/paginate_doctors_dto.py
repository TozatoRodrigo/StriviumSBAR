from pydantic import BaseModel, Field


class PaginateDoctorsDTO(BaseModel):
    page: int = Field(default=1, ge=1, description="Página")
    limit: int = Field(default=10, ge=1, description="Limite")
    search: str | None = Field(default=None, description="Busca")
