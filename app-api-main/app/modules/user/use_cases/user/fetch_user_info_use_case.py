from app.modules.user.dtos.responses.user.user_response import UserResponseDTO
from app.modules.user.exceptions.user_not_found_error import UserNotFoundError
from app.modules.user.interfaces.repositories.user_repository import UserRepository
from app.modules.user.mappers.user_mapper import UserMapper
from app.services.token.user_token_service import UserTokenService


class FetchUserInfoUseCase:
    def __init__(
        self,
        token_service: UserTokenService,
        user_repository: UserRepository,
        user_mapper: UserMapper,
    ) -> None:
        self.current_user_id = token_service.get_user_id_from_token()
        self.user_repository = user_repository
        self.user_mapper = user_mapper

    def handle(self) -> UserResponseDTO:
        try:
            user = self.user_repository.find_by_id(self.current_user_id)
        except Exception as e:
            msg = "Não foi possível buscar as informações do usuário"
            raise UserNotFoundError(msg) from e

        return self.user_mapper.to_response(user)
