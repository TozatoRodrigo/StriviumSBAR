import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.core.environment import envs
from app.main import app
from app.modules.sbar.services.ollama_sbar_extractor import OllamaSbarExtractor
from app.tests.tenant import create_tenant_access_token

client = TestClient(app)


def test_extract_sbar_returns_valid_fallback_json_when_ai_is_disabled(
    monkeypatch: pytest.MonkeyPatch,
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

    response = client.post(
        "/api/sbar/extract", headers=headers, json={"transcript": " "}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["warnings"] == ["Transcrição vazia."]
    assert data["missing_information"] == ["Texto ditado pelo médico."]
    assert data["confidence"]["situation"] == 0


def test_extract_sbar_discards_non_grounded_content_and_recalculates_confidence() -> (
    None
):
    transcript = (
        "Paciente com dor abdominal e febre, recebeu analgésico e antibiótico. "
        "Reavaliar amanhã com raio x."
    )
    raw_response = {
        "message": {
            "content": {
                "situation": {
                    "value": "Paciente com sepse grave.",
                    "evidence": ["Paciente com sepse grave"],
                },
                "background": {"value": "", "evidence": []},
                "assessment": {
                    "value": "Recebeu analgésico e antibiótico.",
                    "evidence": ["recebeu analgésico e antibiótico"],
                },
                "recommendation": {
                    "value": "Manter conduta.",
                    "evidence": ["antibiótico"],
                },
                "plan": {
                    "value": "Reavaliar amanhã com raio x.",
                    "evidence": ["Reavaliar amanhã com raio x"],
                },
                "missing_information": [],
                "warnings": [],
            }
        }
    }

    data = OllamaSbarExtractor.parse_ollama_response(raw_response, transcript)

    assert not data.situation
    assert data.assessment
    assert data.plan
    assert (
        "Situação: conteúdo removido por não estar explícito no ditado."
        in data.warnings
    )
    assert data.confidence.situation == 0
    assert data.confidence.background == 0
    assert data.confidence.assessment > 0
    assert data.confidence.recommendation > 0
    assert data.confidence.plan > 0
