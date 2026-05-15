import pytest
from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient

from app.enums.models.hospitalization_action_status_enums import (
    HospitalizationActionStatus,
)
from app.enums.models.hospitalization_action_type_enums import HospitalizationActionType
from app.main import app
from app.tests.hospitalization import create_hospitalization
from app.tests.hospitalization_action import create_hospitalization_action
from app.tests.tenant import (
    create_role_without_permissions,
    create_tenant,
    create_tenant_access_token,
)
from app.tests.tenant_user import create_tenant_user
from app.tests.user import create_user

fake = Faker()

client = TestClient(app)


def test_create_hospitalization_action_should_return_201_when_valid() -> None:
    hospitalization = create_hospitalization()
    tenant_access_token = create_tenant_access_token(
        {"tenant_id": hospitalization.tenant_id}
    )
    headers = {"Authorization": f"Bearer {tenant_access_token}"}
    data = {
        "description": fake.text(max_nb_chars=100),
    }
    response = client.post(
        f"/hospitalization/v1/hospitalizations/{hospitalization.id}/hospitalization-actions",
        headers=headers,
        data=data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] is not None
    assert data["hospitalization_id"] == str(hospitalization.id)
    assert data["description"] == data["description"]
    assert data["status"] == HospitalizationActionStatus.COMPLETED.value
    assert data["type"] == HospitalizationActionType.HOSPITALIZATION_VISIT.value


def test_create_hospitalization_action_with_sbar_should_return_201_when_valid() -> None:
    hospitalization = create_hospitalization()
    tenant_access_token = create_tenant_access_token(
        {"tenant_id": hospitalization.tenant_id}
    )
    headers = {"Authorization": f"Bearer {tenant_access_token}"}
    data = {
        "description": "SBAR: paciente estável, manter conduta e revisar exames.",
        "action_type": HospitalizationActionType.HOSPITALIZATION_VISIT.value,
        "sbar_situation": "Paciente internado por pneumonia, afebril nas últimas 24h.",
        "sbar_background": "DPOC, em antibioticoterapia desde a admissão.",
        "sbar_assessment": "Evolução estável, sem sinais atuais de insuficiência respiratória.",
        "sbar_recommendation": "Manter antibiótico, fisioterapia respiratória e reavaliar PCR.",
        "sbar_priority": "attention",
        "sbar_clinical_course": "stable",
        "sbar_pending_items": "Aguardar resultado de cultura.",
        "sbar_alerts": "Avisar equipe se saturação ficar abaixo de 92%.",
    }
    response = client.post(
        f"/hospitalization/v1/hospitalizations/{hospitalization.id}/hospitalization-actions",
        headers=headers,
        data=data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data["id"] is not None
    assert response_data["hospitalization_id"] == str(hospitalization.id)
    assert response_data["description"] == data["description"]
    assert (
        response_data["type"] == HospitalizationActionType.HOSPITALIZATION_VISIT.value
    )
    assert response_data["sbar"]["situation"] == data["sbar_situation"]
    assert response_data["sbar"]["background"] == data["sbar_background"]
    assert response_data["sbar"]["assessment"] == data["sbar_assessment"]
    assert response_data["sbar"]["recommendation"] == data["sbar_recommendation"]
    assert response_data["sbar"]["priority"] == data["sbar_priority"]
    assert response_data["sbar"]["clinical_course"] == data["sbar_clinical_course"]
    assert response_data["sbar"]["pending_items"] == data["sbar_pending_items"]
    assert response_data["sbar"]["alerts"] == data["sbar_alerts"]


def test_create_hospitalization_action_with_ai_sbar_requires_review_confirmation() -> (
    None
):
    hospitalization = create_hospitalization()
    tenant_access_token = create_tenant_access_token(
        {"tenant_id": hospitalization.tenant_id}
    )
    headers = {"Authorization": f"Bearer {tenant_access_token}"}
    data = {
        "description": "SBAR gerado por ditado.",
        "action_type": HospitalizationActionType.HOSPITALIZATION_VISIT.value,
        "sbar_situation": "Paciente sem febre.",
        "sbar_assessment": "Evolução estável.",
        "sbar_recommendation": "Manter conduta.",
        "sbar_priority": "routine",
        "sbar_source_transcript": "paciente sem febre evolução estável manter conduta",
        "sbar_ai_generated": "true",
    }

    response = client.post(
        f"/hospitalization/v1/hospitalizations/{hospitalization.id}/hospitalization-actions",
        headers=headers,
        data=data,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_hospitalization_action_with_confirmed_ai_sbar_persists_audit_metadata() -> (
    None
):
    hospitalization = create_hospitalization()
    tenant_access_token = create_tenant_access_token(
        {"tenant_id": hospitalization.tenant_id}
    )
    headers = {"Authorization": f"Bearer {tenant_access_token}"}
    data = {
        "description": "SBAR gerado por ditado e revisado.",
        "action_type": HospitalizationActionType.HOSPITALIZATION_VISIT.value,
        "sbar_situation": "Paciente sem febre.",
        "sbar_assessment": "Evolução estável.",
        "sbar_recommendation": "Manter conduta.",
        "sbar_plan": "Reavaliar amanhã.",
        "sbar_priority": "routine",
        "sbar_source_transcript": "paciente sem febre evolução estável manter conduta reavaliar amanhã",
        "sbar_ai_generated": "true",
        "sbar_ai_review_confirmed": "true",
        "sbar_ai_warnings": '["Revisar dose do antibiótico."]',
        "sbar_ai_missing_information": '["Sinais vitais completos."]',
        "sbar_ai_confidence": '{"situation":0.9,"background":0,"assessment":0.8,"recommendation":0.7,"plan":0.7}',
    }

    response = client.post(
        f"/hospitalization/v1/hospitalizations/{hospitalization.id}/hospitalization-actions",
        headers=headers,
        data=data,
    )

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data["sbar"]["plan"] == data["sbar_plan"]
    assert response_data["sbar"]["source_transcript"] == data["sbar_source_transcript"]
    assert response_data["sbar"]["ai_generated"] is True
    assert response_data["sbar"]["ai_review_confirmed"] is True
    assert response_data["sbar"]["ai_warnings"] == ["Revisar dose do antibiótico."]
    assert response_data["sbar"]["ai_missing_information"] == [
        "Sinais vitais completos."
    ]
    situation_confidence = response_data["sbar"]["ai_confidence"]["situation"]
    assert situation_confidence == pytest.approx(0.9)


def test_update_hospitalization_action_should_return_200_when_valid() -> None:
    hospitalization_action = create_hospitalization_action()
    tenant_access_token = create_tenant_access_token(
        {"tenant_id": hospitalization_action.tenant_id}
    )
    headers = {"Authorization": f"Bearer {tenant_access_token}"}
    data = {
        "description": fake.text(max_nb_chars=100),
    }
    response = client.put(
        f"/hospitalization/v1/hospitalizations/{hospitalization_action.hospitalization_id}/hospitalization-actions/{hospitalization_action.id}",
        headers=headers,
        data=data,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(hospitalization_action.id)
    assert data["hospitalization_id"] == str(hospitalization_action.hospitalization_id)
    assert data["description"] == data["description"]
    assert data["status"] == HospitalizationActionStatus.COMPLETED.value
    assert data["type"] == HospitalizationActionType.HOSPITALIZATION_VISIT.value


def test_update_hospitalization_action_with_sbar_should_return_200_when_valid() -> None:
    hospitalization_action = create_hospitalization_action()
    tenant_access_token = create_tenant_access_token(
        {"tenant_id": hospitalization_action.tenant_id}
    )
    headers = {"Authorization": f"Bearer {tenant_access_token}"}
    data = {
        "description": "SBAR atualizado: paciente melhor, seguir plano.",
        "action_type": HospitalizationActionType.HOSPITALIZATION_VISIT.value,
        "sbar_situation": "Paciente sem febre e com menor demanda de oxigênio.",
        "sbar_background": "Tratamento para pneumonia iniciado há 72h.",
        "sbar_assessment": "Melhora clínica progressiva.",
        "sbar_recommendation": "Reduzir oxigênio conforme tolerância e repetir raio-x.",
        "sbar_priority": "routine",
        "sbar_clinical_course": "improved",
        "sbar_pending_items": "Reavaliar necessidade de antibiótico no dia seguinte.",
        "sbar_alerts": "Atenção a piora de dispneia.",
    }
    response = client.put(
        f"/hospitalization/v1/hospitalizations/{hospitalization_action.hospitalization_id}/hospitalization-actions/{hospitalization_action.id}",
        headers=headers,
        data=data,
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["id"] == str(hospitalization_action.id)
    assert response_data["description"] == data["description"]
    assert response_data["sbar"]["situation"] == data["sbar_situation"]
    assert response_data["sbar"]["priority"] == data["sbar_priority"]
    assert response_data["sbar"]["clinical_course"] == data["sbar_clinical_course"]


def test_paginate_hospitalization_actions_should_return_200_when_valid() -> None:
    hospitalization = create_hospitalization()
    tenant = create_tenant()
    create_hospitalization_action(
        {"hospitalization_id": hospitalization.id, "tenant_id": tenant.id}
    )
    create_hospitalization_action(
        {"hospitalization_id": hospitalization.id, "tenant_id": tenant.id}
    )
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    headers = {"Authorization": f"Bearer {tenant_access_token}"}
    response = client.get(
        f"/hospitalization/v1/hospitalizations/{hospitalization.id}/hospitalization-actions",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    pagination = response.json()
    assert len(pagination["data"]) == 2  # noqa: PLR2004
    assert pagination["total"] == 2  # noqa: PLR2004
    assert pagination["page"] == 1
    assert pagination["limit"] == 10  # noqa: PLR2004
    assert pagination["total_pages"] == 1
    data: dict = pagination["data"][0]
    structure = {
        "id",
        "hospitalization_id",
        "description",
        "status",
        "type",
        "created_at",
        "updated_at",
    }
    assert structure.issubset(data.keys())


def test_get_hospitalization_action_should_return_200_when_valid() -> None:
    hospitalization = create_hospitalization()
    tenant = create_tenant()
    user = create_user()
    tenant_user = create_tenant_user(
        {
            "tenant_id": tenant.id,
            "user_id": user.id,
        }
    )
    hospitalization_action = create_hospitalization_action(
        {
            "hospitalization_id": hospitalization.id,
            "tenant_id": tenant.id,
            "user_id": user.id,
        }
    )
    tenant_access_token = create_tenant_access_token(
        {"tenant_id": tenant.id, "user_id": user.id}
    )
    headers = {"Authorization": f"Bearer {tenant_access_token}"}
    response = client.get(
        f"/hospitalization/v1/hospitalizations/{hospitalization.id}/hospitalization-actions/{hospitalization_action.id}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(hospitalization_action.id)
    assert data["hospitalization_id"] == str(hospitalization.id)
    assert data["description"] == hospitalization_action.description
    assert data["status"] == HospitalizationActionStatus.COMPLETED.value
    assert data["type"] == HospitalizationActionType.HOSPITALIZATION_VISIT.value
    assert data["created_at"] is not None
    assert data["updated_at"] is not None
    assert data["user_id"] == str(user.id)
    assert data["user"]["id"] == str(user.id)
    assert data["user"]["first_name"] == user.first_name
    assert data["user"]["last_name"] == user.last_name
    assert data["user"]["member_type"] == tenant_user.member_type


def test_hospitalization_action_routes_should_return_401_without_token() -> None:
    hospitalization = create_hospitalization()
    response = client.get(
        f"/hospitalization/v1/hospitalizations/{hospitalization.id}/hospitalization-actions"
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_hospitalization_action_should_return_404_when_path_hospitalization_id_mismatches() -> (
    None
):
    tenant = create_tenant()
    hospitalization = create_hospitalization({"tenant_id": tenant.id})
    another_hospitalization = create_hospitalization({"tenant_id": tenant.id})
    hospitalization_action = create_hospitalization_action(
        {"hospitalization_id": hospitalization.id, "tenant_id": tenant.id}
    )
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    headers = {"Authorization": f"Bearer {tenant_access_token}"}

    response = client.get(
        f"/hospitalization/v1/hospitalizations/{another_hospitalization.id}/hospitalization-actions/{hospitalization_action.id}",
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_hospitalization_action_should_return_404_when_path_hospitalization_id_mismatches() -> (
    None
):
    tenant = create_tenant()
    hospitalization = create_hospitalization({"tenant_id": tenant.id})
    another_hospitalization = create_hospitalization({"tenant_id": tenant.id})
    hospitalization_action = create_hospitalization_action(
        {"hospitalization_id": hospitalization.id, "tenant_id": tenant.id}
    )
    tenant_access_token = create_tenant_access_token({"tenant_id": tenant.id})
    headers = {"Authorization": f"Bearer {tenant_access_token}"}

    response = client.put(
        f"/hospitalization/v1/hospitalizations/{another_hospitalization.id}/hospitalization-actions/{hospitalization_action.id}",
        headers=headers,
        data={"description": fake.text(max_nb_chars=100)},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_hospitalization_action_should_return_403_when_permission_is_missing() -> (
    None
):
    tenant = create_tenant()
    user = create_user()
    restricted_role = create_role_without_permissions()
    create_tenant_user(
        {"tenant_id": tenant.id, "user_id": user.id, "role_id": restricted_role.id}
    )
    hospitalization = create_hospitalization(
        {"tenant_id": tenant.id, "user_id": user.id}
    )
    hospitalization_action = create_hospitalization_action(
        {
            "hospitalization_id": hospitalization.id,
            "tenant_id": tenant.id,
            "user_id": user.id,
        }
    )
    tenant_access_token = create_tenant_access_token(
        {"tenant_id": tenant.id, "user_id": user.id}
    )
    headers = {"Authorization": f"Bearer {tenant_access_token}"}

    response = client.put(
        f"/hospitalization/v1/hospitalizations/{hospitalization.id}/hospitalization-actions/{hospitalization_action.id}",
        headers=headers,
        data={"description": fake.text(max_nb_chars=100)},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_hospitalization_action_should_return_403_when_permission_is_missing() -> (
    None
):
    tenant = create_tenant()
    user = create_user()
    restricted_role = create_role_without_permissions()
    create_tenant_user(
        {"tenant_id": tenant.id, "user_id": user.id, "role_id": restricted_role.id}
    )
    hospitalization = create_hospitalization(
        {"tenant_id": tenant.id, "user_id": user.id}
    )
    hospitalization_action = create_hospitalization_action(
        {
            "hospitalization_id": hospitalization.id,
            "tenant_id": tenant.id,
            "user_id": user.id,
        }
    )
    tenant_access_token = create_tenant_access_token(
        {"tenant_id": tenant.id, "user_id": user.id}
    )
    headers = {"Authorization": f"Bearer {tenant_access_token}"}

    response = client.get(
        f"/hospitalization/v1/hospitalizations/{hospitalization.id}/hospitalization-actions/{hospitalization_action.id}",
        headers=headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_hospitalization_action_should_return_403_when_permission_is_missing() -> (
    None
):
    tenant = create_tenant()
    user = create_user()
    restricted_role = create_role_without_permissions()
    create_tenant_user(
        {"tenant_id": tenant.id, "user_id": user.id, "role_id": restricted_role.id}
    )
    hospitalization = create_hospitalization(
        {"tenant_id": tenant.id, "user_id": user.id}
    )
    tenant_access_token = create_tenant_access_token(
        {"tenant_id": tenant.id, "user_id": user.id}
    )
    headers = {"Authorization": f"Bearer {tenant_access_token}"}

    response = client.post(
        f"/hospitalization/v1/hospitalizations/{hospitalization.id}/hospitalization-actions",
        headers=headers,
        data={"description": fake.text(max_nb_chars=100)},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
