from sqlmodel import Session, select

from app.enums.models.roles_names_enum import RolesNamesEnum
from app.models.role import Role


class RoleRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_doctor_role(self) -> Role | None:
        return self.session.exec(
            select(Role).where(Role.name == RolesNamesEnum.DOCTOR.value)
        ).first()
