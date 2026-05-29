from sqlmodel import Session, select

from app.core.database import engine
from app.enums.models.roles_names_enum import RolesNamesEnum
from app.models.role import Role


def get_admin_role() -> Role:
    with Session(engine) as session:
        return session.exec(
            select(Role).where(Role.name == RolesNamesEnum.ADMIN)
        ).first()


def get_doctor_role() -> Role:
    with Session(engine) as session:
        return session.exec(
            select(Role).where(Role.name == RolesNamesEnum.DOCTOR)
        ).first()
