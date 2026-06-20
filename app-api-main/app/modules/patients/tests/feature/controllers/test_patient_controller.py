from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.tests.patient import create_patient
from app.tests.tenant import create_tenant, create_tenant_access_token

fake = Faker()

client = TestClient(app)


def test_create_a_new_patient_should_return_201() -> None:
    tenant = create_tenant()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    data = {
        "first_name": fake.name(),
        "last_name": fake.name(),
        "document_number": None,
        "birth_date": fake.date_of_birth().isoformat(),
    }
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    response = client.post(
        "/patient/v1/patients",
        json=data,
        headers=headers,
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_paginate_patients_should_return_200() -> None:
    tenant = create_tenant()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    patient1 = create_patient({"tenant_id": tenant.id, "first_name": "John"})
    patient2 = create_patient({"tenant_id": tenant.id, "first_name": "Jane"})
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    response = client.get(
        "/patient/v1/patients",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == 2  # noqa: PLR2004
    names = [data[0]["first_name"], data[1]["first_name"]]
    assert patient1.first_name in names
    assert patient2.first_name in names


def test_paginate_patients_with_search_should_return_200() -> None:
    tenant = create_tenant()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    patient = create_patient(
        {
            "tenant_id": tenant.id,
            "first_name": "Jane",
        }
    )
    create_patient({"tenant_id": tenant.id, "first_name": "John", "last_name": "Doe"})
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    params = {"search": patient.first_name}
    response = client.get(
        "/patient/v1/patients",
        params=params,
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == 1
    assert data[0]["id"] == str(patient.id)


def test_paginate_patients_with_search_by_id_should_return_200() -> None:
    tenant = create_tenant()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    patient = create_patient({"tenant_id": tenant.id})
    create_patient({"tenant_id": tenant.id})
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    params = {"search": str(patient.id)}
    response = client.get(
        "/patient/v1/patients",
        params=params,
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == 1
    assert data[0]["id"] == str(patient.id)


def test_get_patient_should_return_200() -> None:
    tenant = create_tenant()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    patient = create_patient(
        {"tenant_id": tenant.id, "first_name": "John", "last_name": "Doe"}
    )
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    response = client.get(
        f"/patient/v1/patients/{patient.id}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(patient.id)
    assert data["first_name"] == patient.first_name
    assert data["last_name"] == patient.last_name


def test_get_patient_should_return_404_when_patient_not_found() -> None:
    from uuid import uuid4  # noqa: PLC0415

    tenant = create_tenant()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    fake_patient_id = uuid4()
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    response = client.get(
        f"/patient/v1/patients/{fake_patient_id}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_patient_should_return_200() -> None:
    tenant = create_tenant()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    patient = create_patient(
        {"tenant_id": tenant.id, "first_name": "John", "last_name": "Doe"}
    )
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "document_number": "12345678900",
        "birth_date": fake.date_of_birth().isoformat(),
    }
    response = client.put(
        f"/patient/v1/patients/{patient.id}",
        json=data,
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["id"] == str(patient.id)
    assert response_data["first_name"] == data["first_name"]
    assert response_data["last_name"] == data["last_name"]
    assert response_data["document_number"] == data["document_number"]


def test_update_patient_should_return_404_when_patient_not_found() -> None:
    from uuid import uuid4  # noqa: PLC0415

    tenant = create_tenant()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    fake_patient_id = uuid4()
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "document_number": None,
        "birth_date": fake.date_of_birth().isoformat(),
    }
    response = client.put(
        f"/patient/v1/patients/{fake_patient_id}",
        json=data,
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
