from uuid import UUID

from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.database import engine
from app.enums.models.roles_names_enum import RolesNamesEnum
from app.main import app
from app.models.role import Role
from app.models.tenant import Tenant
from app.models.tenant_user import TenantUser
from app.tests.tenant import create_tenant, create_tenant_access_token
from app.tests.tenant_user import create_tenant_user
from app.tests.user import create_access_token, create_user

client = TestClient(app)


def test_create_tenant_should_return_200_when_tenant_is_valid() -> None:
    user = create_user()
    access_token = create_access_token(user)
    headers = {"Authorization": f"Bearer {access_token}"}

    payload = {
        "name": "Teste",
    }
    response = client.post("/tenant/v1/tenants", data=payload, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    tenant_id = UUID(response.json()["id"])

    with Session(engine) as session:
        tenant = session.exec(select(Tenant).where(Tenant.id == tenant_id)).first()

        assert tenant is not None
        assert tenant.name == payload["name"]

        tenant_user = session.exec(
            select(TenantUser).where(
                TenantUser.tenant_id == tenant_id,
                TenantUser.user_id == user.id,
            ),
        ).first()
        assert tenant_user is not None
        role = session.exec(select(Role).where(Role.id == tenant_user.role_id)).first()
        assert role is not None
        assert role.name == RolesNamesEnum.ADMIN


def test_list_tenants_should_return_empty_list_when_user_has_no_tenants() -> None:
    user = create_user()
    access_token = create_access_token(user)
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/tenant/v1/tenants/available-for-user", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == []


def test_list_tenants_should_return_tenants_when_user_has_tenants() -> None:
    user = create_user()
    tenant = create_tenant()
    create_tenant()
    create_tenant_user({"user_id": user.id, "tenant_id": tenant.id})
    access_token = create_access_token(user)
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/tenant/v1/tenants/available-for-user", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == 1
    assert data[0]["id"] == str(tenant.id)
    assert data[0]["name"] == tenant.name
    assert data[0]["logo_url"] == tenant.logo_url


def test_get_tenant_should_return_200_when_tenant_is_valid() -> None:
    tenant = create_tenant()
    access_token = create_tenant_access_token({"tenant_id": tenant.id})
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get(f"/tenant/v1/tenants/{tenant.id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(tenant.id)
    assert data["name"] == tenant.name
