from fastapi import status
from fastapi.testclient import TestClient

from app.core.environment import envs
from app.main import app
from app.modules.sbar.services.ollama_sbar_extractor import OllamaSbarExtractor
from app.tests.tenant import create_tenant_access_token

client = TestClient(app)


def test_extract_sbar_returns_valid_fallback_json_when_ai_is_disabled(
    monkeypatch,
) -> None:
    monkeypatch.setattr(envs, "SBAR_AI_ENABLED", False)
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


def test_extract_sbar_normalizes_confidence_from_zero_to_ten_scale() -> None:
    raw_response = {
        "message": {
            "content": {
                "situation": "Paciente estável.",
                "background": "",
                "assessment": "Sem febre, nega dor.",
                "recommendation": "Manter conduta.",
                "plan": "Reavaliar amanhã.",
                "missing_information": [],
                "warnings": [],
                "confidence": {
                    "situation": 8,
                    "background": 0,
                    "assessment": 9,
                    "recommendation": 0.7,
                    "plan": 7,
                },
            }
        }
    }

    data = OllamaSbarExtractor._parse_ollama_response(raw_response)

    assert data.confidence.situation == 0.8
    assert data.confidence.background == 0
    assert data.confidence.assessment == 0.9
    assert data.confidence.recommendation == 0.7
    assert data.confidence.plan == 0.7
