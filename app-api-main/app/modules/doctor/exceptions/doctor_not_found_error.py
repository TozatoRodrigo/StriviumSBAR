from fastapi import status

from app.exceptions.client_aware_error import ClientAwareError


class DoctorNotFoundError(ClientAwareError):
    def __init__(self, message: str = "Médico não encontrado") -> None:
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)
