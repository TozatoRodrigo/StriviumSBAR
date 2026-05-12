import json
import logging
from typing import Any

import httpx

from app.core.environment import envs
from app.modules.sbar.dtos.sbar_extract_dto import (
    SbarExtractContext,
    SbarExtractResponse,
)

log = logging.getLogger("logger")

SYSTEM_PROMPT = """
Você é um extrator de informações clínicas para organização de evolução médica em formato SBAR.
Sua tarefa é apenas reorganizar o texto fornecido pelo médico.
Não crie fatos novos.
Não sugira condutas que não estejam explícitas ou fortemente implícitas no texto.
Se uma informação não estiver presente, retorne string vazia no campo correspondente.
Se houver ambiguidade, adicione em missing_information.
Mantenha linguagem médica objetiva.
Preserve negações clínicas como "sem febre", "nega dor", "sem dispneia".
Retorne apenas JSON válido conforme o schema.
""".strip()


class OllamaSbarExtractor:
    def __init__(
        self,
        enabled: bool | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout_seconds: float | None = None,
    ) -> None:
        self.enabled = envs.SBAR_AI_ENABLED if enabled is None else enabled
        self.base_url = (base_url or envs.OLLAMA_BASE_URL).rstrip("/")
        self.model = model or envs.OLLAMA_MODEL
        self.timeout_seconds = timeout_seconds or envs.OLLAMA_TIMEOUT_SECONDS

    def extract(
        self, transcript: str, context: SbarExtractContext | None = None
    ) -> SbarExtractResponse:
        normalized_transcript = transcript.strip()
        if not normalized_transcript:
            return SbarExtractResponse.fallback(
                warnings=["Transcrição vazia."],
                missing_information=["Texto ditado pelo médico."],
            )

        if not self.enabled:
            return SbarExtractResponse.fallback(
                warnings=["Extração automática por IA está desativada."]
            )

        try:
            response = httpx.post(
                f"{self.base_url}/api/chat",
                json=self._build_payload(normalized_transcript, context),
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
            return self._parse_ollama_response(response.json())
        except Exception:
            log.exception("SBAR extraction failed")
            return SbarExtractResponse.fallback(
                warnings=[
                    "Não foi possível organizar o ditado automaticamente. "
                    "Revise a transcrição manualmente."
                ]
            )

    def _build_payload(
        self, transcript: str, context: SbarExtractContext | None
    ) -> dict[str, Any]:
        user_prompt = self._build_user_prompt(transcript, context)
        return {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "format": SbarExtractResponse.model_json_schema(),
            "options": {"temperature": 0},
        }

    @staticmethod
    def _build_user_prompt(transcript: str, context: SbarExtractContext | None) -> str:
        context_lines = []
        if context and context.hospitalization_id:
            context_lines.append(f"hospitalization_id: {context.hospitalization_id}")

        context_text = "\n".join(context_lines) if context_lines else "Sem contexto adicional."
        return (
            "Contexto opcional da internação:\n"
            f"{context_text}\n\n"
            "Texto bruto ditado pelo médico:\n"
            f"{transcript}"
        )

    @staticmethod
    def _parse_ollama_response(raw_response: dict[str, Any]) -> SbarExtractResponse:
        content = raw_response.get("message", {}).get("content")
        if isinstance(content, str):
            data = json.loads(content)
        elif isinstance(content, dict):
            data = content
        else:
            message = "Ollama response does not contain JSON content"
            raise TypeError(message)

        return SbarExtractResponse.model_validate(data)


def get_sbar_extractor() -> OllamaSbarExtractor:
    return OllamaSbarExtractor()
