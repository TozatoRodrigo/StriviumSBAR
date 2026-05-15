from uuid import UUID

from fastapi import status
from fastapi.testclient import TestClient
from jose import jwt

from app.core.database import get_session
from app.core.environment import envs
from app.main import app
from app.modules.auth.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.modules.auth.utils.jwt import generate_refresh_token
from app.tests.tenant import create_refresh_token as create_tenant_refresh_token
from app.tests.tenant import create_tenant
from app.tests.tenant_user import create_admin_tenant_user
from app.tests.user import create_refresh_token, create_user

client = TestClient(app)


def _decode_refresh_token(refresh_token: str) -> dict:
    return jwt.decode(refresh_token, envs.JWT_SECRET, algorithms=["HS256"])


def _revoke_refresh_token(refresh_token: str) -> None:
    payload = _decode_refresh_token(refresh_token)
    session = next(get_session())
    try:
        RefreshTokenRepository(session).revoke(UUID(payload["jti"]))
    finally:
        session.close()


def _is_refresh_token_revoked(refresh_token: str) -> bool:
    payload = _decode_refresh_token(refresh_token)
    session = next(get_session())
    try:
        return RefreshTokenRepository(session).is_revoked(UUID(payload["jti"]))
    finally:
        session.close()


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


def test_refresh_user_auth_should_return_401_when_refresh_token_is_invalid() -> None:
    response = client.post("/auth/v1/refresh/user", json={"refresh_token": "invalid"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_user_auth_should_return_401_when_refresh_token_type_is_wrong() -> None:
    user = create_user()
    tenant = create_tenant()
    create_admin_tenant_user(user.id, tenant.id)
    tenant_refresh_token = create_tenant_refresh_token(
        {"user_id": user.id, "tenant_id": tenant.id}
    )
    response = client.post(
        "/auth/v1/refresh/user", json={"refresh_token": tenant_refresh_token}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_tenant_auth_should_return_401_when_refresh_token_type_is_wrong() -> (
    None
):
    user_refresh_token = create_refresh_token()
    response = client.post(
        "/auth/v1/refresh/tenant", json={"refresh_token": user_refresh_token}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_user_auth_should_return_401_when_jti_is_missing_in_strict_mode() -> (
    None
):
    user = create_user()
    refresh_token_without_jti = generate_refresh_token(
        {"sub": str(user.id), "type": "user-refresh"}
    )
    response = client.post(
        "/auth/v1/refresh/user", json={"refresh_token": refresh_token_without_jti}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_tenant_auth_should_return_401_when_jti_is_missing_in_strict_mode() -> (
    None
):
    user = create_user()
    tenant = create_tenant()
    create_admin_tenant_user(user.id, tenant.id)

    refresh_token_without_jti = generate_refresh_token(
        {
            "sub": str(tenant.id),
            "type": "tenant-refresh",
            "user_id": str(user.id),
        }
    )
    response = client.post(
        "/auth/v1/refresh/tenant", json={"refresh_token": refresh_token_without_jti}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_user_auth_should_return_401_when_jti_is_revoked() -> None:
    refresh_token = create_refresh_token()
    _revoke_refresh_token(refresh_token)
    response = client.post(
        "/auth/v1/refresh/user", json={"refresh_token": refresh_token}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_tenant_auth_should_return_401_when_jti_is_revoked() -> None:
    user = create_user()
    tenant = create_tenant()
    create_admin_tenant_user(user.id, tenant.id)
    refresh_token = create_tenant_refresh_token(
        {"user_id": user.id, "tenant_id": tenant.id}
    )
    _revoke_refresh_token(refresh_token)

    response = client.post(
        "/auth/v1/refresh/tenant", json={"refresh_token": refresh_token}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_user_auth_should_revoke_family_when_revoked_token_is_reused() -> None:
    original_refresh_token = create_refresh_token()
    first_refresh_response = client.post(
        "/auth/v1/refresh/user", json={"refresh_token": original_refresh_token}
    )
    assert first_refresh_response.status_code == status.HTTP_200_OK
    rotated_refresh_token = first_refresh_response.json()["refresh_token"]

    replay_response = client.post(
        "/auth/v1/refresh/user", json={"refresh_token": original_refresh_token}
    )
    assert replay_response.status_code == status.HTTP_401_UNAUTHORIZED

    family_token_response = client.post(
        "/auth/v1/refresh/user", json={"refresh_token": rotated_refresh_token}
    )
    assert family_token_response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_tenant_auth_should_revoke_family_when_revoked_token_is_reused() -> (
    None
):
    user = create_user()
    tenant = create_tenant()
    create_admin_tenant_user(user.id, tenant.id)
    original_refresh_token = create_tenant_refresh_token(
        {"user_id": user.id, "tenant_id": tenant.id}
    )

    first_refresh_response = client.post(
        "/auth/v1/refresh/tenant",
        json={"refresh_token": original_refresh_token},
    )
    assert first_refresh_response.status_code == status.HTTP_200_OK
    rotated_refresh_token = first_refresh_response.json()["refresh_token"]

    replay_response = client.post(
        "/auth/v1/refresh/tenant",
        json={"refresh_token": original_refresh_token},
    )
    assert replay_response.status_code == status.HTTP_401_UNAUTHORIZED

    family_token_response = client.post(
        "/auth/v1/refresh/tenant",
        json={"refresh_token": rotated_refresh_token},
    )
    assert family_token_response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_user_auth_should_return_401_when_jti_owner_mismatches_payload_sub() -> (
    None
):
    user = create_user()
    another_user = create_user()
    original_refresh_token = create_refresh_token(user)
    original_payload = _decode_refresh_token(original_refresh_token)
    forged_refresh_token = generate_refresh_token(
        {"sub": str(another_user.id), "type": "user-refresh"},
        jti=UUID(original_payload["jti"]),
    )

    forged_response = client.post(
        "/auth/v1/refresh/user", json={"refresh_token": forged_refresh_token}
    )
    assert forged_response.status_code == status.HTTP_401_UNAUTHORIZED

    original_response = client.post(
        "/auth/v1/refresh/user", json={"refresh_token": original_refresh_token}
    )
    assert original_response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_user_auth_should_return_401_when_jti_token_type_mismatches_record() -> (
    None
):
    user = create_user()
    tenant = create_tenant()
    create_admin_tenant_user(user.id, tenant.id)
    original_refresh_token = create_tenant_refresh_token(
        {"user_id": user.id, "tenant_id": tenant.id}
    )
    original_payload = _decode_refresh_token(original_refresh_token)
    forged_refresh_token = generate_refresh_token(
        {"sub": str(user.id), "type": "user-refresh"},
        jti=UUID(original_payload["jti"]),
    )

    forged_response = client.post(
        "/auth/v1/refresh/user", json={"refresh_token": forged_refresh_token}
    )
    assert forged_response.status_code == status.HTTP_401_UNAUTHORIZED

    original_response = client.post(
        "/auth/v1/refresh/tenant", json={"refresh_token": original_refresh_token}
    )
    assert original_response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_tenant_auth_should_return_401_when_jti_owner_mismatches_payload_user_id() -> (
    None
):
    user = create_user()
    another_user = create_user()
    tenant = create_tenant()
    create_admin_tenant_user(user.id, tenant.id)
    original_refresh_token = create_tenant_refresh_token(
        {"user_id": user.id, "tenant_id": tenant.id}
    )
    original_payload = _decode_refresh_token(original_refresh_token)
    forged_refresh_token = generate_refresh_token(
        {
            "sub": str(tenant.id),
            "type": "tenant-refresh",
            "user_id": str(another_user.id),
        },
        jti=UUID(original_payload["jti"]),
    )

    forged_response = client.post(
        "/auth/v1/refresh/tenant", json={"refresh_token": forged_refresh_token}
    )
    assert forged_response.status_code == status.HTTP_401_UNAUTHORIZED

    original_response = client.post(
        "/auth/v1/refresh/tenant", json={"refresh_token": original_refresh_token}
    )
    assert original_response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout_should_return_204_and_revoke_refresh_token_when_valid() -> None:
    refresh_token = create_refresh_token()
    assert _is_refresh_token_revoked(refresh_token) is False

    response = client.post("/auth/v1/logout", json={"refresh_token": refresh_token})

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert _is_refresh_token_revoked(refresh_token) is True


def test_logout_should_return_204_when_refresh_token_is_invalid() -> None:
    response = client.post("/auth/v1/logout", json={"refresh_token": "invalid"})

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_logout_should_return_204_when_refresh_token_has_no_jti() -> None:
    user = create_user()
    refresh_token_without_jti = generate_refresh_token(
        {"sub": str(user.id), "type": "user-refresh"}
    )

    response = client.post(
        "/auth/v1/logout", json={"refresh_token": refresh_token_without_jti}
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_logout_should_return_204_when_refresh_token_has_malformed_jti() -> None:
    user = create_user()
    refresh_token_with_invalid_jti = generate_refresh_token(
        {"sub": str(user.id), "type": "user-refresh", "jti": "invalid-jti"}
    )

    response = client.post(
        "/auth/v1/logout", json={"refresh_token": refresh_token_with_invalid_jti}
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
