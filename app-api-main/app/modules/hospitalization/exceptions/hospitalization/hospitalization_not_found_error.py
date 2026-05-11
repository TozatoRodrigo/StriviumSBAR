from uuid import UUID

from fastapi import status

from app.exceptions.client_aware_error import ClientAwareError


class HospitalizationNotFoundError(ClientAwareError):
    def __init__(self, hospitalization_id: UUID) -> None:
        super().__init__(
            f"Hospitalização com id {hospitalization_id} não encontrada",
            status.HTTP_404_NOT_FOUND,
        )
