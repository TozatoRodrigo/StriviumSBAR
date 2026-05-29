from uuid import uuid4

import pytest

from app.modules.sbar.dtos.sbar_extract_dto import SbarExtractContext
from app.modules.sbar.services.ollama_sbar_extractor import (
    SBAR_EXTRACTION_SCHEMA,
    SYSTEM_PROMPT,
    OllamaSbarExtractor,
)


def test_system_prompt_contains_explicit_sbar_mapping_rules() -> None:
    assert "Mapeamento obrigatório dos campos SBAR" in SYSTEM_PROMPT
    assert "situation:" in SYSTEM_PROMPT
    assert "background:" in SYSTEM_PROMPT
    assert "assessment:" in SYSTEM_PROMPT
    assert "recommendation:" in SYSTEM_PROMPT
    assert "plan:" in SYSTEM_PROMPT
    assert "evidence" in SYSTEM_PROMPT


def test_extract_builds_delimited_user_prompt_with_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    transcript = "Paciente sem febre hoje, manter antibiótico e reavaliar amanhã."
    hospitalization_id = uuid4()
    context = SbarExtractContext(hospitalization_id=hospitalization_id)
    captured_payload: dict[str, object] = {}

    class ResponseStub:
        @staticmethod
        def raise_for_status() -> None:
            return None

        @staticmethod
        def json() -> dict[str, object]:
            return {
                "message": {
                    "content": {
                        "situation": {
                            "value": "Paciente sem febre hoje.",
                            "evidence": ["Paciente sem febre hoje"],
                        },
                        "background": {"value": "", "evidence": []},
                        "assessment": {
                            "value": "Evolução estável.",
                            "evidence": ["evolução estável"],
                        },
                        "recommendation": {
                            "value": "Manter antibiótico.",
                            "evidence": ["manter antibiótico"],
                        },
                        "plan": {
                            "value": "Reavaliar amanhã.",
                            "evidence": ["reavaliar amanhã"],
                        },
                        "missing_information": [],
                        "warnings": [],
                    }
                }
            }

    def post_stub(
        _url: str, *, json: dict[str, object], timeout: float
    ) -> ResponseStub:
        _ = timeout
        captured_payload.update(json)
        return ResponseStub()

    monkeypatch.setattr(
        "app.modules.sbar.services.ollama_sbar_extractor.httpx.post",
        post_stub,
    )

    extractor = OllamaSbarExtractor(
        enabled=True,
        base_url="http://ollama.local",
        model="unit-test-model",
        timeout_seconds=2,
    )
    extractor.extract(transcript, context)

    messages = captured_payload["messages"]
    user_message_content = messages[1]["content"]
    response_schema = captured_payload["format"]

    assert str(hospitalization_id) in user_message_content
    assert "<transcript>" in user_message_content
    assert "</transcript>" in user_message_content
    assert transcript in user_message_content
    assert "Reorganize estritamente o conteúdo acima em SBAR." in user_message_content
    assert response_schema == SBAR_EXTRACTION_SCHEMA


def test_parse_ollama_response_removes_non_grounded_content() -> None:
    transcript = "Paciente com dor abdominal e febre, recebeu analgésico."
    raw_response = {
        "message": {
            "content": {
                "situation": {
                    "value": "Paciente com sepse grave.",
                    "evidence": ["Paciente com sepse grave"],
                },
                "background": {"value": "", "evidence": []},
                "assessment": {"value": "", "evidence": []},
                "recommendation": {"value": "", "evidence": []},
                "plan": {"value": "", "evidence": []},
                "missing_information": [],
                "warnings": [],
            }
        }
    }

    parsed = OllamaSbarExtractor.parse_ollama_response(raw_response, transcript)

    assert not parsed.situation
    assert (
        "Situação: conteúdo removido por não estar explícito no ditado."
        in parsed.warnings
    )
    assert "Situação não informada no ditado." in parsed.missing_information
    assert parsed.confidence.situation == 0


def test_parse_ollama_response_recalculates_confidence_from_grounded_evidence() -> None:
    transcript = (
        "Paciente com dor abdominal e febre. Recebeu analgésico e antibiótico. "
        "Reavaliar amanhã com raio x."
    )
    raw_response = {
        "message": {
            "content": {
                "situation": {
                    "value": "Paciente com dor abdominal e febre.",
                    "evidence": ["Paciente com dor abdominal e febre"],
                },
                "background": {"value": "", "evidence": []},
                "assessment": {
                    "value": "Recebeu analgésico e antibiótico.",
                    "evidence": ["Recebeu analgésico e antibiótico"],
                },
                "recommendation": {
                    "value": "Manter antibiótico.",
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

    parsed = OllamaSbarExtractor.parse_ollama_response(raw_response, transcript)

    assert parsed.situation
    assert parsed.assessment
    assert parsed.plan
    assert parsed.confidence.situation > 0
    assert parsed.confidence.assessment > 0
    assert parsed.confidence.plan > 0
    assert parsed.confidence.background == 0
