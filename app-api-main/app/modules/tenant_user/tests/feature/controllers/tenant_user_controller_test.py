from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.tests.tenant import (
    create_tenant_access_token,
    create_tenant_user,
)

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
