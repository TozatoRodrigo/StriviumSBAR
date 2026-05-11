from fastapi import status

from app.exceptions.client_aware_error import ClientAwareError


class PatientNotFoundError(ClientAwareError):
    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)
