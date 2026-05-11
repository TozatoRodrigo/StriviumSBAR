from uuid import UUID

from app.models.user import User
from app.modules.user.interfaces.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def get_user_by_login(self, login: str) -> User | None:
        return self.user_repository.get_user_by_login(login)

    def get_user_by_id(self, user_id: UUID) -> User | None:
        return self.user_repository.find_by_id(user_id)
