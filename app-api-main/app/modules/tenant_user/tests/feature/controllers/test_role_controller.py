from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.tests.tenant import (
    create_role_without_permissions,
    create_tenant,
    create_tenant_access_token,
)
from app.tests.tenant_user import create_tenant_user
from app.tests.user import create_user

client = TestClient(app)


def test_list_roles_should_return_200() -> None:
    tenant = create_tenant()
    token = create_tenant_access_token({"tenant_id": tenant.id})
    response = client.get(
        "/tenant-user/v1/roles",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) > 0
    role = data[0]
    assert role["id"] is not None
    assert role["name"] is not None
    assert role["description"] is not None


def test_list_roles_should_return_401_without_token() -> None:
    response = client.get("/tenant-user/v1/roles")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_roles_should_return_403_when_permission_is_missing() -> None:
    tenant = create_tenant()
    user = create_user()
    restricted_role = create_role_without_permissions()
    create_tenant_user(
        {"tenant_id": tenant.id, "user_id": user.id, "role_id": restricted_role.id}
    )
    token = create_tenant_access_token({"tenant_id": tenant.id, "user_id": user.id})

    response = client.get(
        "/tenant-user/v1/roles",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
