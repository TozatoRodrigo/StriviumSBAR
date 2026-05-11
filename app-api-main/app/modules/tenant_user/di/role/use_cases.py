from typing import Annotated

from fastapi import Depends

from app.modules.tenant_user.di.role.mappers import get_role_mapper
from app.modules.tenant_user.di.role.repositories import get_role_repository
from app.modules.tenant_user.mappers.role_mapper import RoleMapper
from app.modules.tenant_user.repositories.role_repository import RoleRepository
from app.modules.tenant_user.use_cases.role.list_roles_use_case import ListRolesUseCase


def get_list_roles_use_case(
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
    role_mapper: Annotated[RoleMapper, Depends(get_role_mapper)],
) -> ListRolesUseCase:
    return ListRolesUseCase(role_repository, role_mapper)
