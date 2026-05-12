from uuid import UUID

from pydantic import ConfigDict, Field

from app.concerns.base_model import BaseModel


class SbarExtractContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hospitalization_id: UUID | None = Field(default=None)


class SbarExtractRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    transcript: str = Field(default="")
    context: SbarExtractContext | None = Field(default=None)


class SbarConfidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    situation: float = Field(default=0, ge=0, le=1)
    background: float = Field(default=0, ge=0, le=1)
    assessment: float = Field(default=0, ge=0, le=1)
    recommendation: float = Field(default=0, ge=0, le=1)
    plan: float = Field(default=0, ge=0, le=1)


class SbarExtractResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    situation: str = Field(default="")
    background: str = Field(default="")
    assessment: str = Field(default="")
    recommendation: str = Field(default="")
    plan: str = Field(default="")
    missing_information: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    confidence: SbarConfidence = Field(default_factory=SbarConfidence)

    @classmethod
    def fallback(
        cls, warnings: list[str], missing_information: list[str] | None = None
    ) -> "SbarExtractResponse":
        return cls(
            missing_information=missing_information or ["Revisar transcrição manualmente."],
            warnings=warnings,
            confidence=SbarConfidence(),
        )
