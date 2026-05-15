from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.tests.medical_team import create_medical_team
from app.tests.medical_team_user import create_medical_team_user
from app.tests.tenant import (
    create_role_without_permissions,
    create_tenant,
    create_tenant_access_token,
)
from app.tests.tenant_user import create_tenant_user
from app.tests.user import create_user

fake = Faker()

client = TestClient(app)


def test_create_a_new_medical_team_should_return_200_when_data_is_valid() -> None:
    tenant = create_tenant()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    data = {
        "name": fake.name(),
        "description": fake.sentence(),
    }
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    response = client.post(
        "/medical-team/v1/medical-teams",
        json=data,
        headers=headers,
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_paginate_medical_teams_should_return_200() -> None:
    tenant = create_tenant()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    medical_team = create_medical_team({"tenant_id": tenant.id})
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    response = client.get(
        "/medical-team/v1/medical-teams",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["id"] == str(medical_team.id)
    assert data["data"][0]["name"] == medical_team.name
    assert data["data"][0]["description"] == medical_team.description
    assert data["data"][0]["status"] == medical_team.status.value


def test_get_medical_team_by_id_should_return_200() -> None:
    tenant = create_tenant()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    medical_team = create_medical_team({"tenant_id": tenant.id})
    user = create_user()
    medical_team_user = create_medical_team_user(
        {"tenant_id": tenant.id, "medical_team_id": medical_team.id, "user_id": user.id}
    )
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    response = client.get(
        f"/medical-team/v1/medical-teams/{medical_team.id}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(medical_team.id)
    assert data["name"] == medical_team.name
    assert data["description"] == medical_team.description
    assert data["status"] == medical_team.status.value
    assert data["medical_team_users"][0]["id"] == str(medical_team_user.id)
    assert data["medical_team_users"][0]["first_name"] == user.first_name
    assert data["medical_team_users"][0]["last_name"] == user.last_name
    assert data["medical_team_users"][0]["email"] == user.email
    assert data["medical_team_users"][0]["status"] == medical_team_user.status.value
    assert (
        data["medical_team_users"][0]["created_at"]
        == medical_team_user.created_at.isoformat()
    )
    assert (
        data["medical_team_users"][0]["updated_at"]
        == medical_team_user.updated_at.isoformat()
    )


def test_update_medical_team_should_return_200() -> None:
    medical_team = create_medical_team()
    tenant_access_token = create_tenant_access_token(
        {"tenant_id": medical_team.tenant_id}
    )
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    payload = {
        "name": fake.name(),
        "description": fake.sentence(),
    }
    response = client.put(
        f"/medical-team/v1/medical-teams/{medical_team.id}",
        json=payload,
        headers=headers,
    )
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]


def test_medical_team_routes_should_return_401_without_token() -> None:
    response = client.get("/medical-team/v1/medical-teams")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_medical_team_from_other_tenant_should_return_404() -> None:
    tenant = create_tenant()
    another_tenant = create_tenant()
    medical_team = create_medical_team({"tenant_id": another_tenant.id})
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    response = client.get(
        f"/medical-team/v1/medical-teams/{medical_team.id}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_medical_team_from_other_tenant_should_return_404() -> None:
    tenant = create_tenant()
    another_tenant = create_tenant()
    medical_team = create_medical_team({"tenant_id": another_tenant.id})
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    payload = {
        "name": fake.name(),
        "description": fake.sentence(),
    }
    response = client.put(
        f"/medical-team/v1/medical-teams/{medical_team.id}",
        json=payload,
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_medical_team_should_return_403_when_permission_is_missing() -> None:
    tenant = create_tenant()
    user = create_user()
    restricted_role = create_role_without_permissions()
    create_tenant_user(
        {"tenant_id": tenant.id, "user_id": user.id, "role_id": restricted_role.id}
    )
    tenant_access_token = create_tenant_access_token(
        {"tenant_id": tenant.id, "user_id": user.id}
    )
    headers = {"Authorization": f"Bearer {tenant_access_token}"}

    response = client.post(
        "/medical-team/v1/medical-teams",
        json={"name": fake.name(), "description": fake.sentence()},
        headers=headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_medical_team_should_return_403_when_permission_is_missing() -> None:
    tenant = create_tenant()
    user = create_user()
    restricted_role = create_role_without_permissions()
    create_tenant_user(
        {"tenant_id": tenant.id, "user_id": user.id, "role_id": restricted_role.id}
    )
    medical_team = create_medical_team({"tenant_id": tenant.id})
    tenant_access_token = create_tenant_access_token(
        {"tenant_id": tenant.id, "user_id": user.id}
    )
    headers = {"Authorization": f"Bearer {tenant_access_token}"}

    response = client.get(
        f"/medical-team/v1/medical-teams/{medical_team.id}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
