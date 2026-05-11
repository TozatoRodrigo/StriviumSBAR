from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.database import engine
from app.enums.models.tenant_user_invite_status_enum import TenantUserInviteStatusEnum
from app.main import app
from app.models.tenant_user import TenantUser
from app.models.tenant_user_invite import TenantUserInvite
from app.tests.role import get_admin_role
from app.tests.tenant import create_tenant, create_tenant_access_token
from app.tests.tenant_user_invite import create_tenant_user_invite
from app.tests.user import create_access_token, create_user

fake = Faker()

client = TestClient(app)


def test_send_user_invite_should_return_202_accepted() -> None:
    tenant = create_tenant()
    role = get_admin_role()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    email = fake.email()
    response = client.post(
        "/tenant-user/v1/tenant-users/invite",
        json={
            "email": email,
            "role_id": str(role.id),
        },
        headers={"Authorization": f"Bearer {tenant_access_token}"},
    )
    assert response.status_code == status.HTTP_202_ACCEPTED
    with Session(engine) as session:
        tenant_user_invite = session.exec(
            select(TenantUserInvite).where(
                TenantUserInvite.email == email,
                TenantUserInvite.tenant_id == tenant.id,
                TenantUserInvite.role_id == role.id,
            )
        ).first()
        assert tenant_user_invite is not None


def test_send_invite_to_current_user_should_return_400() -> None:
    tenant = create_tenant()
    user = create_user()
    role = get_admin_role()
    tenant_access_token = create_tenant_access_token(
        {"tenant_id": tenant.id, "user_id": user.id}
    )
    response = client.post(
        "/tenant-user/v1/tenant-users/invite",
        json={
            "email": user.email,
            "role_id": str(role.id),
        },
        headers={"Authorization": f"Bearer {tenant_access_token}"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    with Session(engine) as session:
        tenant_user_invite = session.exec(
            select(TenantUserInvite).where(
                TenantUserInvite.email == user.email,
                TenantUserInvite.tenant_id == tenant.id,
                TenantUserInvite.role_id == role.id,
            )
        ).first()
        assert tenant_user_invite is None


def test_get_pending_invites_should_return_200() -> None:
    user = create_user()
    tenant = create_tenant()
    user_access_token = create_access_token(user)
    invite = create_tenant_user_invite({"email": user.email, "tenant_id": tenant.id})
    response = client.get(
        "/tenant-user/v1/tenant-users/pending-invites",
        headers={"Authorization": f"Bearer {user_access_token}"},
    )
    data = response.json()["data"]
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 1
    assert data[0]["email"] == invite.email
    assert data[0]["email"] == user.email
    assert data[0]["status"] == invite.status.value
    assert data[0]["created_at"] is not None
    assert data[0]["updated_at"] is not None
    assert data[0]["tenant_id"] == str(invite.tenant_id)
    assert data[0]["tenant"]["id"] == str(tenant.id)
    assert data[0]["tenant"]["name"] == tenant.name
    assert data[0]["tenant"]["logo_url"] == tenant.logo_url


def test_accept_invite_should_return_200() -> None:
    user = create_user()
    user_access_token = create_access_token(user)
    invite = create_tenant_user_invite({"email": user.email})
    response = client.post(
        f"/tenant-user/v1/tenant-users/accept-invite/{invite.id}",
        headers={"Authorization": f"Bearer {user_access_token}"},
    )
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["email"] == invite.email
    assert data["email"] == user.email
    assert data["status"] == TenantUserInviteStatusEnum.ACCEPTED.value
    assert data["created_at"] is not None
    assert data["updated_at"] is not None
    with Session(engine) as session:
        tenant_user = session.exec(
            select(TenantUser).where(
                TenantUser.tenant_id == invite.tenant_id,
                TenantUser.user_id == user.id,
                TenantUser.role_id == invite.role_id,
            )
        ).first()
        assert tenant_user is not None


def test_get_pending_invites_count_should_return_200() -> None:
    user = create_user()
    user_access_token = create_access_token(user)
    invites = [
        create_tenant_user_invite({"email": user.email}),
        create_tenant_user_invite({"email": user.email}),
    ]
    response = client.get(
        "/tenant-user/v1/tenant-users/pending-invites/count",
        headers={"Authorization": f"Bearer {user_access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == len(invites)


def test_reject_invite_should_return_200() -> None:
    user = create_user()
    user_access_token = create_access_token(user)
    invite = create_tenant_user_invite({"email": user.email})
    response = client.post(
        f"/tenant-user/v1/tenant-users/reject-invite/{invite.id}",
        headers={"Authorization": f"Bearer {user_access_token}"},
    )
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["email"] == invite.email
    assert data["email"] == user.email
    assert data["status"] == TenantUserInviteStatusEnum.REJECTED.value
    assert data["created_at"] is not None
    assert data["updated_at"] is not None
    with Session(engine) as session:
        tenant_user = session.exec(
            select(TenantUser).where(
                TenantUser.tenant_id == invite.tenant_id,
                TenantUser.user_id == user.id,
                TenantUser.role_id == invite.role_id,
            )
        ).first()
        assert tenant_user is None


def test_get_tenant_pending_invites_should_return_200() -> None:
    tenant = create_tenant()
    user_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    create_tenant_user_invite({"tenant_id": tenant.id})
    response = client.get(
        "/tenant-user/v1/tenant-users/invites",
        headers={"Authorization": f"Bearer {user_access_token}"},
    )
    data = response.json()["data"]
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 1
    assert data[0]["email"] is not None
    assert data[0]["email"] is not None
    assert data[0]["status"] == TenantUserInviteStatusEnum.PENDING.value
    assert data[0]["created_at"] is not None
    assert data[0]["updated_at"] is not None
    assert data[0]["tenant_id"] == str(tenant.id)
    assert data[0]["tenant"]["id"] == str(tenant.id)
    assert data[0]["tenant"]["name"] == tenant.name
    assert data[0]["tenant"]["logo_url"] == tenant.logo_url
