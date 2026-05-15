from uuid import uuid4

from faker import Faker
from sqlmodel import Session, select

from app.core.database import engine, get_session
from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.tenant import Tenant
from app.models.tenant_user import TenantUser
from app.models.user import User
from app.modules.auth.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.modules.auth.services.refresh_token.refresh_token_service import (
    RefreshTokenService,
)
from app.modules.auth.utils.jwt import (
    REFRESH_TOKEN_EXPIRES_MINUTES,
    generate_access_token,
    generate_refresh_token,
)
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


def create_role_without_permissions() -> Role:
    role = Role(
        name=f"restricted-{uuid4()}",
        description="Role without permissions for authorization tests",
    )
    with Session(engine) as session:
        session.add(role)
        session.commit()
        session.refresh(role)
    return role


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
        tenant = session.exec(select(Tenant).where(Tenant.id == tenant_id)).first()
        user = session.exec(select(User).where(User.id == user_id)).first()
    if tenant_user is None:
        tenant_user = create_tenant_user({"user_id": user_id, "tenant_id": tenant_id})
        with Session(engine) as session:
            tenant = session.exec(select(Tenant).where(Tenant.id == tenant_id)).first()
            user = session.exec(select(User).where(User.id == user_id)).first()
            tenant_user = session.exec(
                select(TenantUser).where(
                    TenantUser.user_id == user_id, TenantUser.tenant_id == tenant_id
                )
            ).first()

    with Session(engine) as session:
        role = session.exec(select(Role).where(Role.id == tenant_user.role_id)).first()
        permissions = session.exec(
            select(Permission)
            .join(RolePermission)
            .where(RolePermission.role_id == tenant_user.role_id)
        ).all()

    tenant_name = tenant.name if tenant else fake.name()
    if user:
        user_first_name = user.first_name
        user_last_name = user.last_name
        user_email = user.email
    else:
        user_first_name = fake.first_name()
        user_last_name = fake.last_name()
        user_email = fake.email()

    role_name = role.name if role else "admin"
    role_id = str(role.id) if role else ""

    payload = {
        "sub": str(tenant_id),
        "type": "tenant",
        "tenant": {
            "id": str(tenant_id),
            "name": tenant_name,
        },
        "user": {
            "id": str(user_id),
            "first_name": user_first_name,
            "last_name": user_last_name,
            "email": user_email,
        },
        "role": {
            "id": role_id,
            "name": role_name,
            "permissions": [
                {
                    "code": permission.code,
                    "name": permission.name,
                }
                for permission in permissions
            ],
        },
    }
    return generate_access_token(payload)


def create_refresh_token(data: dict | None = None) -> str:
    if data is None:
        data = {}
    user_id = data["user_id"] if "user_id" in data else create_user().id
    tenant_id = data["tenant_id"] if "tenant_id" in data else create_tenant().id
    session = next(get_session())
    refresh_token_repository = RefreshTokenRepository(session)
    refresh_token_service = RefreshTokenService(refresh_token_repository)
    jti, _token_family = refresh_token_service.create_token_record(
        user_id=user_id,
        token_type="tenant-refresh",  # noqa: S106
        expires_minutes=REFRESH_TOKEN_EXPIRES_MINUTES,
    )
    session.close()

    payload = {
        "sub": str(tenant_id),
        "type": "tenant-refresh",
        "user_id": str(user_id),
    }
    return generate_refresh_token(payload, jti=jti)
