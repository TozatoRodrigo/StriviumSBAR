from uuid import uuid4

from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient

from app.enums.models.hospitalization_status_enums import HospitalizationStatus
from app.main import app
from app.tests.hospitalization import create_hospitalization
from app.tests.medical_team import create_medical_team
from app.tests.patient import create_patient
from app.tests.tenant import create_tenant, create_tenant_access_token
from app.tests.user import create_user

fake = Faker()

client = TestClient(app)


def test_create_a_new_hospitalization_should_return_201() -> None:
    tenant = create_tenant()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    patient = create_patient({"tenant_id": tenant.id})
    medical_team = create_medical_team({"tenant_id": tenant.id})
    data = {
        "patient_id": str(patient.id),
        "medical_team_id": str(medical_team.id),
        "hospitalization_number": fake.name(),
        "hospitalization_place": fake.name(),
        "hospitalization_sector": fake.name(),
        "hospitalization_reason": fake.name(),
        "observation": fake.name(),
    }
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    response = client.post(
        "/hospitalization/v1/hospitalizations",
        json=data,
        headers=headers,
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_paginate_hospitalizations_should_return_200() -> None:
    tenant = create_tenant()
    user = create_user()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    patient = create_patient({"tenant_id": tenant.id})
    medical_team = create_medical_team({"tenant_id": tenant.id})
    hospitalization = create_hospitalization(
        {
            "tenant_id": tenant.id,
            "user_id": user.id,
            "patient_id": patient.id,
            "medical_team_id": medical_team.id,
        }
    )
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    response = client.get(
        "/hospitalization/v1/hospitalizations",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    hospitalization_response = data["data"][0]
    assert hospitalization_response["id"] == str(hospitalization.id)
    assert hospitalization_response["user_id"] == str(user.id)
    assert hospitalization_response["medical_team_id"] == str(medical_team.id)
    assert hospitalization_response["status"] == "active"
    assert hospitalization_response["number"] == hospitalization.hospitalization_number
    assert hospitalization_response["place"] == hospitalization.hospitalization_place
    assert hospitalization_response["sector"] == hospitalization.hospitalization_sector
    assert hospitalization_response["patient"]["id"] == str(patient.id)
    assert hospitalization_response["patient"]["first_name"] == patient.first_name
    assert hospitalization_response["patient"]["last_name"] == patient.last_name


def test_paginate_hospitalizations_with_patient_id_filter_should_return_filtered_results() -> (
    None
):
    """Deve retornar apenas internações do paciente especificado."""
    tenant = create_tenant()
    user = create_user()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    patient1 = create_patient({"tenant_id": tenant.id})
    patient2 = create_patient({"tenant_id": tenant.id})
    medical_team = create_medical_team({"tenant_id": tenant.id})
    hospitalization1 = create_hospitalization(
        {
            "tenant_id": tenant.id,
            "user_id": user.id,
            "patient_id": patient1.id,
            "medical_team_id": medical_team.id,
        }
    )
    hospitalization2 = create_hospitalization(
        {
            "tenant_id": tenant.id,
            "user_id": user.id,
            "patient_id": patient2.id,
            "medical_team_id": medical_team.id,
        }
    )
    hospitalization3 = create_hospitalization(
        {
            "tenant_id": tenant.id,
            "user_id": user.id,
            "patient_id": patient1.id,
            "medical_team_id": medical_team.id,
        }
    )
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    response = client.get(
        f"/hospitalization/v1/hospitalizations?patient_id={patient1.id}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 2  # noqa: PLR2004
    hospitalization_ids = [str(h["id"]) for h in data["data"]]
    assert str(hospitalization1.id) in hospitalization_ids
    assert str(hospitalization3.id) in hospitalization_ids
    assert str(hospitalization2.id) not in hospitalization_ids


def test_paginate_hospitalizations_with_invalid_patient_id_should_return_empty() -> (
    None
):
    """Deve retornar vazio quando o patient_id não existe."""
    tenant = create_tenant()
    user = create_user()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    patient = create_patient({"tenant_id": tenant.id})
    medical_team = create_medical_team({"tenant_id": tenant.id})
    create_hospitalization(
        {
            "tenant_id": tenant.id,
            "user_id": user.id,
            "patient_id": patient.id,
            "medical_team_id": medical_team.id,
        }
    )
    fake_patient_id = uuid4()
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    response = client.get(
        f"/hospitalization/v1/hospitalizations?patient_id={fake_patient_id}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 0


def test_get_hospitalization_should_return_200() -> None:
    tenant = create_tenant()
    user = create_user()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    patient = create_patient({"tenant_id": tenant.id})
    medical_team = create_medical_team({"tenant_id": tenant.id})
    hospitalization = create_hospitalization(
        {
            "tenant_id": tenant.id,
            "user_id": user.id,
            "patient_id": patient.id,
            "medical_team_id": medical_team.id,
        }
    )
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    response = client.get(
        f"/hospitalization/v1/hospitalizations/{hospitalization.id}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(hospitalization.id)
    assert data["user_id"] == str(user.id)
    assert data["patient_id"] == str(patient.id)
    assert data["medical_team_id"] == str(medical_team.id)
    assert data["status"] == "active"
    assert data["number"] == hospitalization.hospitalization_number
    assert data["place"] == hospitalization.hospitalization_place
    assert data["sector"] == hospitalization.hospitalization_sector
    assert data["reason"] == hospitalization.hospitalization_reason
    assert data["observation"] == hospitalization.observation
    assert data["patient"]["id"] == str(patient.id)
    assert data["patient"]["first_name"] == patient.first_name
    assert data["patient"]["last_name"] == patient.last_name


def test_update_hospitalization_should_return_200() -> None:
    tenant = create_tenant()
    user = create_user()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    patient = create_patient({"tenant_id": tenant.id})
    medical_team = create_medical_team({"tenant_id": tenant.id})
    hospitalization = create_hospitalization(
        {
            "tenant_id": tenant.id,
            "user_id": user.id,
            "patient_id": patient.id,
            "medical_team_id": medical_team.id,
        }
    )
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    data = {
        "medical_team_id": str(medical_team.id),
        "number": "UPDATED-123",
        "place": "Updated Place",
        "sector": "Updated Sector",
        "reason": "Updated Reason",
        "observation": "Updated Observation",
    }
    response = client.put(
        f"/hospitalization/v1/hospitalizations/{hospitalization.id}",
        json=data,
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["id"] == str(hospitalization.id)
    assert response_data["medical_team_id"] == data["medical_team_id"]
    assert response_data["number"] == data["number"]
    assert response_data["place"] == data["place"]
    assert response_data["sector"] == data["sector"]
    assert response_data["reason"] == data["reason"]
    assert response_data["observation"] == data["observation"]


def test_update_hospitalization_should_return_404_when_hospitalization_not_found() -> (
    None
):
    tenant = create_tenant()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    medical_team = create_medical_team({"tenant_id": tenant.id})
    fake_hospitalization_id = uuid4()
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    data = {
        "medical_team_id": str(medical_team.id),
        "number": "12345",
        "place": "Some Place",
        "sector": "Some Sector",
        "reason": "Some Reason",
        "observation": "Some Observation",
    }
    response = client.put(
        f"/hospitalization/v1/hospitalizations/{fake_hospitalization_id}",
        json=data,
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_paginate_pendings_hospitalizations_should_return_200() -> None:
    tenant = create_tenant()
    user = create_user()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    patient = create_patient({"tenant_id": tenant.id})
    medical_team = create_medical_team({"tenant_id": tenant.id})
    hospitalization = create_hospitalization(
        {
            "tenant_id": tenant.id,
            "user_id": user.id,
            "patient_id": patient.id,
            "medical_team_id": medical_team.id,
        }
    )
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    response = client.get(
        "/hospitalization/v1/hospitalizations/pendings",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    hospitalization_response = data["data"][0]
    assert hospitalization_response["id"] == str(hospitalization.id)
    assert hospitalization_response["user_id"] == str(user.id)
    assert hospitalization_response["medical_team_id"] == str(medical_team.id)
    assert hospitalization_response["status"] == "active"
    assert hospitalization_response["number"] == hospitalization.hospitalization_number
    assert hospitalization_response["place"] == hospitalization.hospitalization_place
    assert hospitalization_response["sector"] == hospitalization.hospitalization_sector
    assert hospitalization_response["patient"]["id"] == str(patient.id)
    assert hospitalization_response["patient"]["first_name"] == patient.first_name
    assert hospitalization_response["patient"]["last_name"] == patient.last_name


def test_paginate_pendings_hospitalizations_with_search_should_return_200() -> None:
    tenant = create_tenant()
    user = create_user()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    patient = create_patient({"tenant_id": tenant.id})
    medical_team = create_medical_team({"tenant_id": tenant.id})
    hospitalization = create_hospitalization(
        {
            "tenant_id": tenant.id,
            "user_id": user.id,
            "patient_id": patient.id,
            "medical_team_id": medical_team.id,
        }
    )
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    response = client.get(
        "/hospitalization/v1/hospitalizations/pendings",
        params={"search": patient.first_name},
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    hospitalization_response = data["data"][0]
    assert hospitalization_response["id"] == str(hospitalization.id)
    assert hospitalization_response["user_id"] == str(user.id)
    assert hospitalization_response["medical_team_id"] == str(medical_team.id)
    assert hospitalization_response["status"] == "active"
    assert hospitalization_response["number"] == hospitalization.hospitalization_number
    assert hospitalization_response["place"] == hospitalization.hospitalization_place
    assert hospitalization_response["sector"] == hospitalization.hospitalization_sector
    assert hospitalization_response["patient"]["id"] == str(patient.id)
    assert hospitalization_response["patient"]["first_name"] == patient.first_name
    assert hospitalization_response["patient"]["last_name"] == patient.last_name


def test_paginate_pendings_hospitalizations_with_invalid_search_shouldnt_return_results() -> (
    None
):
    tenant = create_tenant()
    user = create_user()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    patient = create_patient(
        {"tenant_id": tenant.id, "first_name": "John", "last_name": "Doe"}
    )
    medical_team = create_medical_team({"tenant_id": tenant.id})
    create_hospitalization(
        {
            "tenant_id": tenant.id,
            "user_id": user.id,
            "patient_id": patient.id,
            "medical_team_id": medical_team.id,
        }
    )
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    response = client.get(
        "/hospitalization/v1/hospitalizations/pendings",
        params={"search": "invalid-search"},
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["data"]) == 0


def test_create_duplicated_hospitalization_should_return_422() -> None:
    tenant = create_tenant()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    patient = create_patient({"tenant_id": tenant.id})
    medical_team = create_medical_team({"tenant_id": tenant.id})
    create_hospitalization(
        {
            "tenant_id": tenant.id,
            "patient_id": patient.id,
            "medical_team_id": medical_team.id,
        }
    )
    data = {
        "patient_id": str(patient.id),
        "medical_team_id": str(medical_team.id),
        "hospitalization_number": fake.name(),
        "hospitalization_place": fake.name(),
        "hospitalization_sector": fake.name(),
        "hospitalization_reason": fake.name(),
        "observation": fake.name(),
    }
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    response = client.post(
        "/hospitalization/v1/hospitalizations",
        json=data,
        headers=headers,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert data["message"] is not None


def test_create_new_hospitalization_with_old_finished_hospitalization_should_return_201() -> (
    None
):
    tenant = create_tenant()
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    patient = create_patient({"tenant_id": tenant.id})
    medical_team = create_medical_team({"tenant_id": tenant.id})
    create_hospitalization(
        {
            "tenant_id": tenant.id,
            "patient_id": patient.id,
            "medical_team_id": medical_team.id,
            "status": HospitalizationStatus.DISCHARGED,
        }
    )
    data = {
        "patient_id": str(patient.id),
        "medical_team_id": str(medical_team.id),
        "hospitalization_number": fake.name(),
        "hospitalization_place": fake.name(),
        "hospitalization_sector": fake.name(),
        "hospitalization_reason": fake.name(),
        "observation": fake.name(),
    }
    headers = {
        "Authorization": f"Bearer {tenant_access_token}",
    }
    response = client.post(
        "/hospitalization/v1/hospitalizations",
        json=data,
        headers=headers,
    )
    assert response.status_code == status.HTTP_201_CREATED
