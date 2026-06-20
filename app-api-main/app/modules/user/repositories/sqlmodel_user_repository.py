from uuid import UUID

from sqlmodel import Session, select

from app.models.user import User
from app.modules.user.interfaces.repositories.user_repository import UserRepository


class SqlModelUserRepository(UserRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def find_by_id(self, user_id: UUID) -> User | None:
        return self.session.exec(select(User).where(User.id == user_id)).first()

    def get_user_by_login(self, login: str) -> User | None:
        return self.session.exec(select(User).where(User.email == login)).first()
