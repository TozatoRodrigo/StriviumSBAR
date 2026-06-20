from app.modules.user.dtos.requests.user.create_user_request_dto import (
    CreateUserRequestDTO,
)
from app.modules.user.dtos.responses.user.user_response import (
    UserResponseDTO,
)
from app.modules.user.interfaces.repositories.user_repository import UserRepository
from app.modules.user.mappers.user_mapper import UserMapper


class CreateUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        user_mapper: UserMapper,
    ) -> None:
        self.user_repository = user_repository
        self.user_mapper = user_mapper

    def handle(self, user_data: CreateUserRequestDTO) -> UserResponseDTO:
        user_entity = self.user_mapper.to_entity(user_data)
        user = self.user_repository.save(user_entity)

        return self.user_mapper.to_response(user)
