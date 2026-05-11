from uuid import UUID

from sqlmodel import Session, select

from app.models.user import User
from app.services.token.user_token_service import UserTokenService


class LoggedUserService:
    def __init__(self, session: Session, user_token_service: UserTokenService) -> None:
        self.session = session
        self.user_token_service = user_token_service

    def get_logged_user(self) -> User:
        user_id = self.user_token_service.get_user_id_from_token()
        return self.session.exec(select(User).where(User.id == UUID(user_id))).first()

    def get_logged_user_by_tenant_token(self) -> User | None:
        user_id = self.user_token_service.get_user_id_from_tenant_token()
        return self.session.exec(select(User).where(User.id == UUID(user_id))).first()
