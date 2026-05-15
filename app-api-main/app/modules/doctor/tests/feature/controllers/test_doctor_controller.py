from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.tests.doctor import create_doctor
from app.tests.tenant import create_tenant, create_tenant_access_token

client = TestClient(app)


def make_payload(
    email: str = "doctor@example.com", document: str = "12345678910"
) -> dict:
    return {
        "full_name": "John Doe",
        "birth_date": "1990-01-01",
        "cellphone": "41999999999",
        "gender": "male",
        "document": document,
        "email": email,
        "specialty": "CARDIOLOGY",
        "crm_uf": "PR",
        "crm_number": "123456",
    }


def test_create_doctor_should_return_201() -> None:
    tenant = create_tenant()
    access_token = create_tenant_access_token({"tenant_id": tenant.id})

    response = client.post(
        "/doctor/v1/doctors",
        json=make_payload(),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["full_name"] == "John Doe"
    assert data["crm_uf"] == "PR"
    assert data["crm_number"] == "123456"


def test_paginate_doctors_should_return_only_tenant_doctors() -> None:
    tenant = create_tenant()
    another_tenant = create_tenant()

    create_doctor(
        {
            "tenant_id": tenant.id,
            "email": "doctor-1@example.com",
            "document": "11111111111",
        }
    )
    create_doctor(
        {
            "tenant_id": tenant.id,
            "email": "doctor-2@example.com",
            "document": "22222222222",
        }
    )
    create_doctor(
        {
            "tenant_id": another_tenant.id,
            "email": "doctor-3@example.com",
            "document": "33333333333",
        }
    )

    access_token = create_tenant_access_token({"tenant_id": tenant.id})
    response = client.get(
        "/doctor/v1/doctors",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == 2  # noqa: PLR2004


def test_get_doctor_should_return_200() -> None:
    tenant = create_tenant()
    doctor = create_doctor({"tenant_id": tenant.id})
    access_token = create_tenant_access_token({"tenant_id": tenant.id})

    response = client.get(
        f"/doctor/v1/doctors/{doctor.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(doctor.id)
    assert data["full_name"] == f"{doctor.first_name} {doctor.last_name}"


def test_get_doctor_from_other_tenant_should_return_404() -> None:
    tenant = create_tenant()
    another_tenant = create_tenant()
    doctor = create_doctor({"tenant_id": another_tenant.id})
    access_token = create_tenant_access_token({"tenant_id": tenant.id})

    response = client.get(
        f"/doctor/v1/doctors/{doctor.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_doctor_should_return_200() -> None:
    tenant = create_tenant()
    doctor = create_doctor(
        {
            "tenant_id": tenant.id,
            "email": "doctor-update@example.com",
            "document": "44444444444",
        }
    )
    access_token = create_tenant_access_token({"tenant_id": tenant.id})

    response = client.put(
        f"/doctor/v1/doctors/{doctor.id}",
        json=make_payload(email="doctor-updated@example.com", document="55555555555"),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "doctor-updated@example.com"
    assert data["document"] == "55555555555"


def test_delete_doctor_should_return_204() -> None:
    tenant = create_tenant()
    doctor = create_doctor({"tenant_id": tenant.id})
    access_token = create_tenant_access_token({"tenant_id": tenant.id})

    response = client.delete(
        f"/doctor/v1/doctors/{doctor.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_doctor_routes_should_return_401_without_token() -> None:
    response = client.get("/doctor/v1/doctors")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_doctor_should_return_403_without_permission() -> None:
    tenant = create_tenant()
    doctor_user = create_doctor(
        {
            "tenant_id": tenant.id,
            "email": "restricted-doctor@example.com",
            "document": "77777777777",
        }
    )
    access_token = create_tenant_access_token(
        {
            "tenant_id": tenant.id,
            "user_id": doctor_user.id,
        }
    )

    response = client.post(
        "/doctor/v1/doctors",
        json=make_payload(email="forbidden@example.com", document="88888888888"),
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
