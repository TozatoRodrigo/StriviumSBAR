from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.tests.tenant import create_tenant_access_token

client = TestClient(app)


def test_extract_sbar_returns_valid_fallback_json_when_ai_is_disabled() -> None:
    tenant_access_token = create_tenant_access_token()
    headers = {"Authorization": f"Bearer {tenant_access_token}"}
    payload = {
        "transcript": "Paciente sem febre, nega dor, manter antibiótico e reavaliar amanhã.",
    }

    response = client.post("/api/sbar/extract", headers=headers, json=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == {
        "situation": "",
        "background": "",
        "assessment": "",
        "recommendation": "",
        "plan": "",
        "missing_information": ["Revisar transcrição manualmente."],
        "warnings": ["Extração automática por IA está desativada."],
        "confidence": {
            "situation": 0,
            "background": 0,
            "assessment": 0,
            "recommendation": 0,
            "plan": 0,
        },
    }


def test_extract_sbar_returns_valid_json_for_empty_transcript() -> None:
    tenant_access_token = create_tenant_access_token()
    headers = {"Authorization": f"Bearer {tenant_access_token}"}

    response = client.post("/api/sbar/extract", headers=headers, json={"transcript": " "})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["warnings"] == ["Transcrição vazia."]
    assert data["missing_information"] == ["Texto ditado pelo médico."]
    assert data["confidence"]["situation"] == 0
