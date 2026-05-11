import logging

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.dtos.exception.exception_dto import ExceptionDTO
from app.exceptions.client_aware_error import ClientAwareError

log = logging.getLogger("logger")


def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    log.error(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content=_to_exception_dto(exc.detail).model_dump(),
    )


def client_aware_error_handler(request: Request, exc: ClientAwareError) -> JSONResponse:
    log.error(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content=_to_exception_dto(exc.message).model_dump(),
    )


def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    log.error(exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_to_exception_dto("Internal server error").model_dump(),
    )


def _to_exception_dto(message: str) -> ExceptionDTO:
    return ExceptionDTO(message=message)
