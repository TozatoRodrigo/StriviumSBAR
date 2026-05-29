from typing import Annotated

from fastapi import Depends, status
from fastapi.responses import JSONResponse

from app.modules.sbar.dtos.sbar_extract_dto import SbarExtractRequest
from app.modules.sbar.services.ollama_sbar_extractor import (
    OllamaSbarExtractor,
    get_sbar_extractor,
)


def extract_sbar(
    data: SbarExtractRequest,
    extractor: Annotated[OllamaSbarExtractor, Depends(get_sbar_extractor)],
) -> JSONResponse:
    result = extractor.extract(data.transcript, data.context)
    return JSONResponse(status_code=status.HTTP_200_OK, content=result.to_json())
