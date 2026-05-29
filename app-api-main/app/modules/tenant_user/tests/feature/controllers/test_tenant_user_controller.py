from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.tests.tenant import (
    create_role_without_permissions,
    create_tenant,
    create_tenant_access_token,
    create_tenant_user,
)
from app.tests.user import create_user

client = TestClient(app)


def test_paginate_tenant_users_should_return_200() -> None:
    tenant_user = create_tenant_user()
    tenant_access_token = create_tenant_access_token(
        {"tenant_id": tenant_user.tenant_id, "user_id": tenant_user.user_id}
    )
    headers = {"Authorization": f"Bearer {tenant_access_token}"}
    response = client.get("/tenant-user/v1/tenant-users", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    pagination = response.json()
    data = pagination["data"]
    assert len(data) == 1
    assert data[0]["id"] == str(tenant_user.id)
    assert data[0]["tenant_id"] == str(tenant_user.tenant_id)
    assert data[0]["user_id"] == str(tenant_user.user_id)
    assert data[0]["role_id"] == str(tenant_user.role_id)
    assert data[0]["created_at"] is not None
    assert data[0]["updated_at"] is not None


def test_paginate_tenant_users_should_return_401_without_token() -> None:
    response = client.get("/tenant-user/v1/tenant-users")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_paginate_tenant_users_should_return_403_when_permission_is_missing() -> None:
    tenant = create_tenant()
    user = create_user()
    restricted_role = create_role_without_permissions()
    create_tenant_user(
        {"tenant_id": tenant.id, "user_id": user.id, "role_id": restricted_role.id}
    )
    tenant_access_token = create_tenant_access_token(
        {"tenant_id": tenant.id, "user_id": user.id}
    )
    response = client.get(
        "/tenant-user/v1/tenant-users",
        headers={"Authorization": f"Bearer {tenant_access_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
