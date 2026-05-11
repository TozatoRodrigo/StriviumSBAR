from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_user_should_return_201_when_user_is_valid(
    mock_turnstile_validation,  # noqa: ANN001
) -> None:
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "crm_state": "SP",
        "crm_number": "123456",
        "document": "11111111111",
        "email": "john.doe@example.com",
        "password": "password",
        "birth_date": "1990-01-01",
    }
    response = client.post(
        "/user/v1/users",
        json=payload,
        headers={"x-turnstile-token": "test-turnstile-token"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    user_data = response.json()
    assert user_data["id"] is not None
    assert user_data["first_name"] == payload["first_name"]
    assert user_data["last_name"] == payload["last_name"]
    assert user_data["crm_state"] == payload["crm_state"]
    assert user_data["crm_number"] == payload["crm_number"]
    assert user_data["document"] == payload["document"]
    assert user_data["email"] == payload["email"]
    assert user_data["birth_date"] == payload["birth_date"]


def test_create_user_should_return_401_when_turnstile_token_is_missing() -> None:
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "crm_state": "SP",
        "crm_number": "123456",
        "document": "11111111111",
        "email": "john.doe@example.com",
        "password": "password",
        "birth_date": "1990-01-01",
    }

    response = client.post(
        "/user/v1/users",
        json=payload,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
