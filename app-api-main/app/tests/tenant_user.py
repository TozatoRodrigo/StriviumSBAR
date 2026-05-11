from uuid import UUID

from sqlmodel import Session, select

from app.core.database import engine
from app.enums.models.roles_names_enum import RolesNamesEnum
from app.enums.models.tenant_user_member_type_enums import TenantUserMemberType
from app.models.role import Role
from app.models.tenant_user import TenantUser
from app.tests.role import get_admin_role
from app.tests.tenant import create_tenant
from app.tests.user import create_user


def create_admin_tenant_user(
    user_id: UUID,
    tenant_id: UUID,
) -> TenantUser:
    with Session(engine) as session:
        role = session.exec(
            select(Role).where(Role.name == RolesNamesEnum.ADMIN)
        ).first()
    if role is None:
        msg = "Role admin not found"
        raise ValueError(msg)
    return create_tenant_user(
        {"role_id": role.id, "user_id": user_id, "tenant_id": tenant_id}
    )


def create_tenant_user(data: dict) -> TenantUser:
    user_id = data["user_id"] if "user_id" in data else create_user().id
    tenant_id = data["tenant_id"] if "tenant_id" in data else create_tenant().id
    role_id = data["role_id"] if "role_id" in data else get_admin_role().id
    member_type = data.get("member_type", TenantUserMemberType.DOCTOR)

    tenant_user = TenantUser(
        user_id=user_id, tenant_id=tenant_id, role_id=role_id, member_type=member_type
    )
    with Session(engine) as session:
        session.add(tenant_user)
        session.commit()
        session.refresh(tenant_user)
    return tenant_user
