from app.models.user import User
from app.modules.user.dtos.requests.user.create_user_request_dto import (
    CreateUserRequestDTO,
)
from app.modules.user.dtos.responses.user.user_response import (
    UserResponseDTO,
)
from app.modules.user.utils.bcrypt import hash_password


class UserMapper:
    @staticmethod
    def to_entity(user_data: CreateUserRequestDTO) -> User:
        return User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            crm_state=user_data.crm_state,
            crm_number=user_data.crm_number,
            document=user_data.document,
            email=user_data.email,
            password=hash_password(user_data.password),
            birth_date=user_data.birth_date,
        )

    @staticmethod
    def to_response(user: User) -> UserResponseDTO:
        return UserResponseDTO(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            crm_state=user.crm_state,
            crm_number=user.crm_number,
            document=user.document,
            email=user.email,
            birth_date=user.birth_date,
        )
