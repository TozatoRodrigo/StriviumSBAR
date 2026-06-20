from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.tests.tenant import create_refresh_token as create_tenant_refresh_token
from app.tests.tenant import create_tenant
from app.tests.tenant_user import create_admin_tenant_user
from app.tests.user import create_refresh_token, create_user

client = TestClient(app)


def test_refresh_user_auth_should_return_200_when_refresh_token_is_valid() -> None:
    refresh_token = create_refresh_token()
    response = client.post(
        "/auth/v1/refresh/user", json={"refresh_token": refresh_token}
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json["access_token"] is not None


def test_refresh_tenant_auth_should_return_200_when_refresh_token_is_valid() -> None:
    user = create_user()
    tenant = create_tenant()
    create_admin_tenant_user(user.id, tenant.id)
    refresh_token = create_tenant_refresh_token(
        {"user_id": user.id, "tenant_id": tenant.id}
    )
    response = client.post(
        "/auth/v1/refresh/tenant", json={"refresh_token": refresh_token}
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json["access_token"] is not None
