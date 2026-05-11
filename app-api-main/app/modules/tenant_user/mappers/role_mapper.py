from app.models.role import Role
from app.modules.tenant_user.dtos.responses.role.list_roles_response import (
    ListRolesResponse,
)
from app.modules.tenant_user.dtos.responses.role.role_response import RoleResponse


class RoleMapper:
    @staticmethod
    def to_response_list(roles: list[Role]) -> ListRolesResponse:
        items = [RoleMapper.to_response(role) for role in roles]
        return ListRolesResponse(data=items)

    @staticmethod
    def to_response(role: Role) -> RoleResponse:
        return RoleResponse(id=role.id, name=role.name, description=role.description)
