from app.modules.tenant_user.dtos.responses.role.list_roles_response import (
    ListRolesResponse,
)
from app.modules.tenant_user.mappers.role_mapper import RoleMapper
from app.modules.tenant_user.repositories.role_repository import RoleRepository


class ListRolesUseCase:
    def __init__(
        self, role_repository: RoleRepository, role_mapper: RoleMapper
    ) -> None:
        self.role_repository = role_repository
        self.role_mapper = role_mapper

    def handle(self) -> ListRolesResponse:
        roles = self.role_repository.list_all()
        return self.role_mapper.to_response_list(roles)
