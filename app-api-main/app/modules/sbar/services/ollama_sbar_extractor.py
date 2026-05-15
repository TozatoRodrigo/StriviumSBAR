import json
import logging
from typing import Any

import httpx

from app.core.environment import envs
from app.exceptions.validation_error import ValidationError
from app.modules.sbar.dtos.sbar_extract_dto import (
    SbarExtractContext,
    SbarExtractResponse,
)

log = logging.getLogger("logger")

SYSTEM_PROMPT = """
Você é um extrator clínico para organizar evolução médica no formato SBAR.

Objetivo:
- Reorganizar exclusivamente a transcrição enviada pelo médico.

Regras inegociáveis:
- Não invente fatos, diagnósticos, exames, medicações, doses ou condutas.
- Não sugira condutas novas; apenas extraia o que já está explícito ou fortemente implícito.
- Se uma informação não existir, deixe o campo como string vazia.
- Se houver ambiguidade, lacuna relevante ou conflito, registre em missing_information e/ou warnings.
- Preserve negações clínicas (ex.: "sem febre", "nega dor", "sem dispneia").
- Preserve referência temporal relevante (ex.: "hoje", "últimas 24h", "amanhã").
- Mantenha linguagem médica objetiva e curta, sem floreios.

Mapeamento obrigatório dos campos SBAR:
- situation: estado atual e motivo clínico principal agora (sinais/sintomas/evolução imediata).
- background: contexto clínico prévio relevante (diagnósticos prévios, comorbidades, histórico útil).
- assessment: interpretação clínica documentada pelo médico (gravidade, resposta, estabilidade/piora/melhora).
- recommendation: recomendações/condutas imediatas descritas.
- plan: próximos passos com horizonte temporal (reavaliação, exames, monitorização, continuidade da conduta).

Critérios de qualidade:
- Evite duplicação desnecessária entre campos.
- Não copie a transcrição inteira para um único campo.
- Se o médico apenas descreve fatos sem interpretação, não force assessment.
- Use confidence como decimal de 0 a 1 (ex.: 0.8; nunca 8).

Formato de saída:
- Retorne apenas JSON válido e estritamente compatível com o schema.
- Não use markdown, não use crases, não adicione texto fora do JSON.
""".strip()

MAX_TEN_POINT_CONFIDENCE = 10
MIN_TEN_POINT_CONFIDENCE = 1


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
            "keep_alive": "30m",
            "options": {"temperature": 0, "num_predict": 700},
        }

    @staticmethod
    def _build_user_prompt(transcript: str, context: SbarExtractContext | None) -> str:
        context_lines = []
        if context and context.hospitalization_id:
            context_lines.append(f"hospitalization_id: {context.hospitalization_id}")

        context_text = (
            "\n".join(context_lines) if context_lines else "Sem contexto adicional."
        )
        return (
            "Contexto opcional da internação:\n"
            f"{context_text}\n\n"
            "Transcrição clínica bruta (não editar):\n"
            "<transcript>\n"
            f"{transcript}\n"
            "</transcript>\n\n"
            "Reorganize estritamente o conteúdo acima em SBAR."
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
            raise ValidationError(message)

        data = OllamaSbarExtractor._normalize_confidence_scale(data)
        return SbarExtractResponse.model_validate(data)

    @staticmethod
    def parse_ollama_response(raw_response: dict[str, Any]) -> SbarExtractResponse:
        return OllamaSbarExtractor._parse_ollama_response(raw_response)

    @staticmethod
    def _normalize_confidence_scale(data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        confidence = data.get("confidence")
        if not isinstance(confidence, dict):
            return data

        normalized_confidence = confidence.copy()
        for field, value in confidence.items():
            if isinstance(value, int | float) and (
                MIN_TEN_POINT_CONFIDENCE < value <= MAX_TEN_POINT_CONFIDENCE
            ):
                normalized_confidence[field] = value / MAX_TEN_POINT_CONFIDENCE

        return {**data, "confidence": normalized_confidence}


def get_sbar_extractor() -> OllamaSbarExtractor:
    return OllamaSbarExtractor()
