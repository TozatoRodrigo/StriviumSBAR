from pydantic import Field

from app.concerns.base_model import BaseModel
from app.modules.tenant.dtos.responses.tenant_response_dto import TenantResponseDTO


class ListTenantsResponseDTO(BaseModel):
    data: list[TenantResponseDTO] = Field(default_factory=list)
