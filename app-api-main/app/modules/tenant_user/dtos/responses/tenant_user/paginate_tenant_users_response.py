from pydantic import Field

from app.concerns.base_model import BaseModel
from app.modules.tenant_user.dtos.responses.tenant_user.detailed_tenant_user_response import (
    DetailedTenantUserResponse,
)


class PaginateTenantUsersResponse(BaseModel):
    data: list[DetailedTenantUserResponse] = Field(description="Lista de usuários")
    total: int = Field(description="Total de usuários", examples=[20])
    page: int = Field(description="Página atual", examples=[1])
    limit: int = Field(description="Limite de usuários", examples=[10])
    total_pages: int = Field(description="Total de páginas", examples=[2])
