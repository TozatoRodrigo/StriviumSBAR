import json
import logging
import re
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
- Não sugira condutas novas.
- Use apenas informações explicitamente presentes no texto bruto.
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
- Não use inferência clínica para "completar" conteúdo ausente.

Formato de saída:
- Retorne apenas JSON válido e estritamente compatível com o schema.
- Não use markdown, não use crases, não adicione texto fora do JSON.
- Para cada campo SBAR, retorne:
  - `value`: texto organizado para o campo
  - `evidence`: lista de trechos literais do ditado que sustentam o `value`
- Se não houver evidência explícita no ditado para um campo, retorne `value: ""` e `evidence: []`.
""".strip()

MAX_TEN_POINT_CONFIDENCE = 10
MIN_TEN_POINT_CONFIDENCE = 1
SBAR_FIELDS = ("situation", "background", "assessment", "recommendation", "plan")
SBAR_FIELD_LABELS = {
    "situation": "Situação",
    "background": "Contexto",
    "assessment": "Avaliação",
    "recommendation": "Recomendação",
    "plan": "Plano",
}
MIN_CONFIDENCE = 0.0
MAX_CONFIDENCE = 0.9
SHORT_TEXT_WORDS_LIMIT = 4
MEDIUM_TEXT_WORDS_LIMIT = 12
MIN_GROUNDED_FRAGMENTS_FOR_BOOST = 2
FIELD_SHAPE_SCHEMA = {
    "type": "object",
    "properties": {
        "value": {"type": "string"},
        "evidence": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["value", "evidence"],
    "additionalProperties": False,
}
SBAR_EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "situation": FIELD_SHAPE_SCHEMA,
        "background": FIELD_SHAPE_SCHEMA,
        "assessment": FIELD_SHAPE_SCHEMA,
        "recommendation": FIELD_SHAPE_SCHEMA,
        "plan": FIELD_SHAPE_SCHEMA,
        "missing_information": {"type": "array", "items": {"type": "string"}},
        "warnings": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "situation",
        "background",
        "assessment",
        "recommendation",
        "plan",
        "missing_information",
        "warnings",
    ],
    "additionalProperties": False,
}


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
            return self._parse_ollama_response(response.json(), normalized_transcript)
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
            "format": SBAR_EXTRACTION_SCHEMA,
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
    def _parse_ollama_response(
        raw_response: dict[str, Any], transcript: str = ""
    ) -> SbarExtractResponse:
        content = raw_response.get("message", {}).get("content")
        if isinstance(content, str):
            data = json.loads(content)
        elif isinstance(content, dict):
            data = content
        else:
            message = "Ollama response does not contain JSON content"
            raise ValidationError(message)

        return OllamaSbarExtractor._build_grounded_response(data, transcript)

    @staticmethod
    def parse_ollama_response(
        raw_response: dict[str, Any], transcript: str = ""
    ) -> SbarExtractResponse:
        return OllamaSbarExtractor._parse_ollama_response(raw_response, transcript)

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

    @staticmethod
    def _build_grounded_response(data: Any, transcript: str) -> SbarExtractResponse:
        parsed = OllamaSbarExtractor._coerce_response_payload(data)
        normalized_transcript = OllamaSbarExtractor._normalize_text(transcript)
        warnings = parsed["warnings"].copy()
        missing_information = parsed["missing_information"].copy()
        field_values: dict[str, str] = {}
        field_confidences: dict[str, float] = {}

        for field in SBAR_FIELDS:
            field_payload = parsed[field]
            extracted = field_payload["value"]
            evidences = field_payload["evidence"]
            grounded_fragments = OllamaSbarExtractor._ground_fragments(
                extracted, evidences, normalized_transcript
            )
            was_cleaned = bool(extracted or evidences) and not bool(grounded_fragments)
            cleaned_value = OllamaSbarExtractor._join_fragments(grounded_fragments)

            if was_cleaned:
                warnings.append(
                    f"{SBAR_FIELD_LABELS[field]}: conteúdo removido por não estar explícito no ditado."
                )

            if not cleaned_value:
                missing_information.append(
                    f"{SBAR_FIELD_LABELS[field]} não informada no ditado."
                )

            field_values[field] = cleaned_value
            field_confidences[field] = OllamaSbarExtractor._calculate_confidence(
                cleaned_value, len(grounded_fragments), was_cleaned
            )

        return SbarExtractResponse(
            situation=field_values["situation"],
            background=field_values["background"],
            assessment=field_values["assessment"],
            recommendation=field_values["recommendation"],
            plan=field_values["plan"],
            warnings=OllamaSbarExtractor._deduplicate_strings(warnings),
            missing_information=OllamaSbarExtractor._deduplicate_strings(
                missing_information
            ),
            confidence=field_confidences,
        )

    @staticmethod
    def _coerce_response_payload(data: Any) -> dict[str, Any]:
        if not isinstance(data, dict):
            message = "Ollama response does not contain JSON object payload"
            raise ValidationError(message)

        normalized_legacy = OllamaSbarExtractor._normalize_confidence_scale(data)
        payload: dict[str, Any] = {
            "warnings": OllamaSbarExtractor._coerce_string_list(
                normalized_legacy.get("warnings")
            ),
            "missing_information": OllamaSbarExtractor._coerce_string_list(
                normalized_legacy.get("missing_information")
            ),
        }

        for field in SBAR_FIELDS:
            raw_field = normalized_legacy.get(field)
            if isinstance(raw_field, dict):
                payload[field] = {
                    "value": OllamaSbarExtractor._coerce_string(raw_field.get("value")),
                    "evidence": OllamaSbarExtractor._coerce_string_list(
                        raw_field.get("evidence")
                    ),
                }
                continue

            payload[field] = {
                "value": OllamaSbarExtractor._coerce_string(raw_field),
                "evidence": [],
            }

        return payload

    @staticmethod
    def _ground_fragments(
        extracted_value: str, evidences: list[str], normalized_transcript: str
    ) -> list[str]:
        grounded = [
            evidence
            for evidence in evidences
            if OllamaSbarExtractor._is_fragment_grounded(
                evidence, normalized_transcript
            )
        ]

        if grounded:
            return OllamaSbarExtractor._deduplicate_strings(grounded)

        fallback_parts = [
            part.strip()
            for part in re.split(r"[.;:\n]+", extracted_value)
            if part and part.strip()
        ]
        grounded_fallback = [
            part
            for part in fallback_parts
            if OllamaSbarExtractor._is_fragment_grounded(part, normalized_transcript)
        ]
        return OllamaSbarExtractor._deduplicate_strings(grounded_fallback)

    @staticmethod
    def _is_fragment_grounded(fragment: str, normalized_transcript: str) -> bool:
        normalized_fragment = OllamaSbarExtractor._normalize_text(fragment)
        if not normalized_fragment:
            return False
        return normalized_fragment in normalized_transcript

    @staticmethod
    def _join_fragments(fragments: list[str]) -> str:
        return re.sub(r"\s+", " ", " ".join(fragments).strip())

    @staticmethod
    def _normalize_text(value: str) -> str:
        lowered = value.lower()
        normalized = re.sub(r"[^\w\s]", " ", lowered, flags=re.UNICODE)
        return re.sub(r"\s+", " ", normalized, flags=re.UNICODE).strip()

    @staticmethod
    def _calculate_confidence(
        cleaned_value: str, grounded_fragments_count: int, was_cleaned: bool
    ) -> float:
        words = len(cleaned_value.split())
        if words == 0:
            return MIN_CONFIDENCE

        if words <= SHORT_TEXT_WORDS_LIMIT:
            confidence = 0.4
        elif words <= MEDIUM_TEXT_WORDS_LIMIT:
            confidence = 0.7
        else:
            confidence = 0.9

        if (
            grounded_fragments_count >= MIN_GROUNDED_FRAGMENTS_FOR_BOOST
            and confidence < MAX_CONFIDENCE
        ):
            confidence += 0.1

        if was_cleaned:
            confidence = max(0.3, confidence - 0.2)

        return round(min(MAX_CONFIDENCE, confidence), 2)

    @staticmethod
    def _coerce_string(value: Any) -> str:
        if isinstance(value, str):
            return value.strip()
        return ""

    @staticmethod
    def _coerce_string_list(value: Any) -> list[str]:
        if not isinstance(value, list):
            return []
        return [
            item.strip() for item in value if isinstance(item, str) and item.strip()
        ]

    @staticmethod
    def _deduplicate_strings(values: list[str]) -> list[str]:
        deduplicated: list[str] = []
        seen = set()
        for value in values:
            normalized = OllamaSbarExtractor._normalize_text(value)
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            deduplicated.append(value.strip())
        return deduplicated


def get_sbar_extractor() -> OllamaSbarExtractor:
    return OllamaSbarExtractor()
