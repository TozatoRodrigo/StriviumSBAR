from app.modules.tenant.dtos.requests.create_tenant_request_dto import (
    CreateTenantRequestDTO,
)
from app.modules.tenant.dtos.responses.tenant_response_dto import TenantResponseDTO
from app.modules.tenant.mappers.tenant_mapper import TenantMapper
from app.modules.tenant.repositories.tenant_repository import TenantRepository
from app.modules.tenant.use_cases.tenant_user.create_admin_tenant_user_use_case import (
    CreateAdminTenantUserUseCase,
)
from app.modules.user.exceptions.user_not_found_error import UserNotFoundError
from app.services.logged_user.logged_user_service import LoggedUserService


class CreateTenantUseCase:
    def __init__(
        self,
        tenant_repository: TenantRepository,
        tenant_mapper: TenantMapper,
        logged_user_service: LoggedUserService,
        create_admin_tenant_user_use_case: CreateAdminTenantUserUseCase,
    ) -> None:
        self.tenant_repository = tenant_repository
        self.tenant_mapper = tenant_mapper
        self.logged_user_service = logged_user_service
        self.create_admin_tenant_user_use_case = create_admin_tenant_user_use_case

    def handle(self, tenant_data: CreateTenantRequestDTO) -> TenantResponseDTO:
        tenant_entity = self.tenant_mapper.to_entity(tenant_data)
        tenant = self.tenant_repository.save(tenant_entity)

        user = self.logged_user_service.get_logged_user()
        if user is None:
            msg = "Usuário não encontrado ou não autenticado"
            raise UserNotFoundError(msg)

        self.create_admin_tenant_user_use_case.handle(tenant.id, user.id)
        return self.tenant_mapper.to_response(tenant)
