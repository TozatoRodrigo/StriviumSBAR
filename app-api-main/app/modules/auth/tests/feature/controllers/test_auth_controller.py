from datetime import date

from fastapi import status
from fastapi.testclient import TestClient

from app.core.database import get_session
from app.main import app
from app.models.user import User
from app.modules.user.utils.bcrypt import hash_password
from app.tests.tenant import create_tenant
from app.tests.tenant_user import create_admin_tenant_user
from app.tests.user import create_access_token, create_user

client = TestClient(app)


def test_login_with_email_should_return_200_when_login_is_valid(
    mock_turnstile_validation,  # noqa: ANN001
) -> None:
    password = "teste"  # noqa: S105
    user = User(
        first_name="teste",
        last_name="teste",
        crm_state="SP",
        crm_number="123456",
        document="1234567890",
        email="teste@teste.com",
        password=hash_password(password),
        birth_date=date(2000, 1, 1),
    )

    session = next(get_session())
    session.add(user)
    session.commit()

    response = client.post(
        "/auth/v1/login",
        json={"login": user.email, "password": password},
        headers={"x-turnstile-token": "test-turnstile-token"},
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json["access_token"] is not None

    session.close()


def test_login_should_return_401_when_login_is_invalid(
    mock_turnstile_validation,  # noqa: ANN001
) -> None:
    password = "teste"  # noqa: S105
    user = User(
        first_name="teste",
        last_name="teste",
        crm_state="SP",
        crm_number="123456",
        document="1234567890",
        email="teste@teste.com",
        password=hash_password(password),
        birth_date=date(2000, 1, 1),
    )

    session = next(get_session())
    session.add(user)
    session.commit()

    response = client.post(
        "/auth/v1/login",
        json={"login": "emailfake@teste.com", "password": "invalid"},
        headers={"x-turnstile-token": "test-turnstile-token"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response_json = response.json()
    assert not hasattr(response_json, "access_token")

    session.close()


def test_login_should_return_401_when_turnstile_token_is_missing() -> None:
    password = "teste"  # noqa: S105
    user = User(
        first_name="teste",
        last_name="teste",
        crm_state="SP",
        crm_number="123456",
        document="1234567890",
        email="teste@teste.com",
        password=hash_password(password),
        birth_date=date(2000, 1, 1),
    )

    session = next(get_session())
    session.add(user)
    session.commit()

    response = client.post(
        "/auth/v1/login", json={"login": user.email, "password": password}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    session.close()


def test_tenant_auth_should_return_200_when_tenant_auth_is_valid() -> None:
    tenant = create_tenant()
    user = create_user()
    create_admin_tenant_user(user.id, tenant.id)
    user_access_token = create_access_token(user)
    response = client.post(
        "/auth/v1/tenant",
        json={"tenant_id": str(tenant.id)},
        headers={"Authorization": f"Bearer {user_access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json["access_token"] is not None
