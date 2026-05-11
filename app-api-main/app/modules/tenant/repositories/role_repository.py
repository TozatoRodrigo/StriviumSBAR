from sqlalchemy.orm import Session
from sqlmodel import select

from app.models.role import Role


class RoleRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_name(self, name: str) -> Role:
        return self.session.exec(select(Role).where(Role.name == name)).first()
