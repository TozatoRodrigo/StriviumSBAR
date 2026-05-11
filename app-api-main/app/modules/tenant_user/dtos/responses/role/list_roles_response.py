from pydantic import Field

from app.concerns.base_model import BaseModel
from app.modules.tenant_user.dtos.responses.role.role_response import RoleResponse


class ListRolesResponse(BaseModel):
    data: list[RoleResponse] = Field(description="Lista de papéis")
