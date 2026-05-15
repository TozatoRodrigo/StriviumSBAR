from uuid import uuid4

import pytest

from app.modules.sbar.dtos.sbar_extract_dto import SbarExtractContext
from app.modules.sbar.services.ollama_sbar_extractor import (
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
                        "situation": "Paciente sem febre hoje.",
                        "background": "",
                        "assessment": "Evolução estável.",
                        "recommendation": "Manter antibiótico.",
                        "plan": "Reavaliar amanhã.",
                        "missing_information": [],
                        "warnings": [],
                        "confidence": {
                            "situation": 0.8,
                            "background": 0,
                            "assessment": 0.7,
                            "recommendation": 0.8,
                            "plan": 0.8,
                        },
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

    assert str(hospitalization_id) in user_message_content
    assert "<transcript>" in user_message_content
    assert "</transcript>" in user_message_content
    assert transcript in user_message_content
    assert "Reorganize estritamente o conteúdo acima em SBAR." in user_message_content
