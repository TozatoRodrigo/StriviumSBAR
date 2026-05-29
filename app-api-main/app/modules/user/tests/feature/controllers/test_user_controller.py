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


def test_create_user_should_return_400_when_email_already_exists(
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

    duplicated_email_payload = {
        **payload,
        "document": "22222222222",
    }
    duplicate_response = client.post(
        "/user/v1/users",
        json=duplicated_email_payload,
        headers={"x-turnstile-token": "test-turnstile-token"},
    )
    assert duplicate_response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        duplicate_response.json()["message"] == "Já existe um usuário com este e-mail"
    )


def test_create_user_should_return_400_when_document_already_exists(
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

    duplicated_document_payload = {
        **payload,
        "email": "other.john.doe@example.com",
    }
    duplicate_response = client.post(
        "/user/v1/users",
        json=duplicated_document_payload,
        headers={"x-turnstile-token": "test-turnstile-token"},
    )
    assert duplicate_response.status_code == status.HTTP_400_BAD_REQUEST
    assert duplicate_response.json()["message"] == "Já existe um usuário com este CPF"
