from datetime import date
from secrets import token_urlsafe
from uuid import UUID

from faker import Faker
from sqlmodel import Session, select

from app.core.database import engine
from app.enums.models.roles_names_enum import RolesNamesEnum
from app.enums.models.tenant_user_member_type_enums import TenantUserMemberType
from app.models.role import Role
from app.models.tenant_user import TenantUser
from app.models.user import User
from app.modules.user.utils.bcrypt import hash_password
from app.tests.tenant import create_tenant

fake = Faker()


def create_doctor(data: dict | None = None) -> User:
    if data is None:
        data = {}

    tenant_id = data["tenant_id"] if "tenant_id" in data else create_tenant().id

    with Session(engine) as session:
        role = session.exec(
            select(Role).where(Role.name == RolesNamesEnum.DOCTOR.value)
        ).first()
        if role is None:
            msg = "Role doctor not found"
            raise ValueError(msg)

        user = User(
            first_name=data.get("first_name", fake.first_name()),
            last_name=data.get("last_name", fake.last_name()),
            crm_state=data.get("crm_state", "PR"),
            crm_number=data.get("crm_number", fake.numerify("######")),
            document=data.get("document", fake.numerify("###########")),
            email=data.get("email", fake.email()),
            password=hash_password(token_urlsafe(24)),
            birth_date=data.get("birth_date", date(1990, 1, 1)),
            cellphone=data.get("cellphone", fake.numerify("4199#######")),
            gender=data.get("gender", "male"),
            specialty=data.get("specialty", "CARDIOLOGY"),
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        tenant_user = TenantUser(
            tenant_id=UUID(str(tenant_id)),
            user_id=user.id,
            role_id=role.id,
            member_type=TenantUserMemberType.DOCTOR,
        )
        session.add(tenant_user)
        session.commit()
        session.refresh(user)
        session.expunge(user)

    return user
