from fastapi import status

from app.exceptions.client_aware_error import ClientAwareError


class MedicalTeamNotFoundError(ClientAwareError):
    def __init__(self, message: str = "Time médico não encontrado") -> None:
        super().__init__(message, status.HTTP_404_NOT_FOUND)
