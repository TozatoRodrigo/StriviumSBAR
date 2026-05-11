from faker import Faker
from sqlmodel import Session

from app.core.database import engine
from app.models.tenant_user_invite import TenantUserInvite
from app.tests.role import get_admin_role
from app.tests.tenant import create_tenant

fake = Faker()


def create_tenant_user_invite(data: dict | None = None) -> TenantUserInvite:
    if data is None:
        data = {}

    tenant_user_invite = TenantUserInvite(
        tenant_id=data.get("tenant_id", create_tenant().id),
        role_id=data.get("role_id", get_admin_role().id),
        email=data.get("email", fake.email()),
    )
    with Session(engine) as session:
        session.add(tenant_user_invite)
        session.commit()
        session.refresh(tenant_user_invite)
    return tenant_user_invite
