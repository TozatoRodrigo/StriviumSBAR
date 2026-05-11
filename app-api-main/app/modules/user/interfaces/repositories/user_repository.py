from abc import ABC, abstractmethod
from uuid import UUID

from app.models.user import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def find_by_id(self, user_id: UUID) -> User | None:
        pass

    @abstractmethod
    def get_user_by_login(self, login: str) -> User | None:
        pass
