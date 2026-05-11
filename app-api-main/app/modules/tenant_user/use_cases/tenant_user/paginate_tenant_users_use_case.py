from uuid import UUID

from app.modules.tenant_user.dtos.responses.tenant_user.paginate_tenant_users_response import (
    PaginateTenantUsersResponse,
)
from app.modules.tenant_user.dtos.tenant_user.paginate_tenant_users_params_dto import (
    PaginateTenantUsersParamsDTO,
)
from app.modules.tenant_user.mappers.tenant_user_mapper import TenantUserMapper
from app.modules.tenant_user.repositories.tenant_user_repository import (
    TenantUserRepository,
)


class PaginateTenantUsersUseCase:
    def __init__(
        self,
        tenant_user_repository: TenantUserRepository,
        tenant_user_mapper: TenantUserMapper,
        tenant_id: UUID,
    ) -> None:
        self.tenant_user_repository = tenant_user_repository
        self.tenant_user_mapper = tenant_user_mapper
        self.tenant_id = tenant_id

    def handle(
        self, params: PaginateTenantUsersParamsDTO
    ) -> PaginateTenantUsersResponse:
        pagination = self.tenant_user_repository.paginate(
            params.page, params.limit, params.search, self.tenant_id
        )
        return self.tenant_user_mapper.to_paginate_response(pagination)
