from faker import Faker
from sqlmodel import Session, select

from app.core.database import engine, get_session
from app.models.tenant import Tenant
from app.models.tenant_user import TenantUser
from app.modules.auth.utils.jwt import generate_access_token, generate_refresh_token
from app.tests.role import get_admin_role
from app.tests.user import create_user

fake = Faker()


def create_tenant() -> Tenant:
    tenant = Tenant(name="Tenant 1", logo_url=None)
    session = next(get_session())
    session.add(tenant)
    session.commit()
    session.refresh(tenant)
    session.close()
    return tenant


def create_tenant_user(data: dict | None = None) -> TenantUser:
    if data is None:
        data = {}
    user_id = data["user_id"] if "user_id" in data else create_user().id
    tenant_id = data["tenant_id"] if "tenant_id" in data else create_tenant().id
    role_id = data["role_id"] if "role_id" in data else get_admin_role().id

    with Session(engine) as session:
        tenant_user = TenantUser(
            user_id=user_id,
            tenant_id=tenant_id,
            role_id=role_id,
        )
        session.add(tenant_user)
        session.commit()
        session.refresh(tenant_user)
    return tenant_user


def create_tenant_access_token(data: dict | None = None) -> str:
    if data is None:
        data = {}
    user_id = data["user_id"] if "user_id" in data else create_user().id
    tenant_id = data["tenant_id"] if "tenant_id" in data else create_tenant().id
    with Session(engine) as session:
        tenant_user = session.exec(
            select(TenantUser).where(
                TenantUser.user_id == user_id, TenantUser.tenant_id == tenant_id
            )
        ).first()
    if tenant_user is None:
        tenant_user = create_tenant_user({"user_id": user_id, "tenant_id": tenant_id})
    payload = {
        "sub": str(tenant_id),
        "type": "tenant",
        "tenant": {
            "id": str(tenant_id),
            "name": fake.name(),
        },
        "user": {
            "id": str(user_id),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
        },
    }
    return generate_access_token(payload)


def create_refresh_token(data: dict | None = None) -> str:
    if data is None:
        data = {}
    user_id = data["user_id"] if "user_id" in data else create_user().id
    tenant_id = data["tenant_id"] if "tenant_id" in data else create_tenant().id
    payload = {
        "sub": str(tenant_id),
        "type": "tenant-refresh",
        "user_id": str(user_id),
    }
    return generate_refresh_token(payload)
