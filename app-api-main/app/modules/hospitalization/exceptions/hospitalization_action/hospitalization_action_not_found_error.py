from uuid import UUID

from fastapi import status

from app.exceptions.client_aware_error import ClientAwareError


class HospitalizationActionNotFoundError(ClientAwareError):
    def __init__(self, hospitalization_action_id: UUID) -> None:
        super().__init__(
            f"Ação da hospitalização com id {hospitalization_action_id} não encontrada",
            status.HTTP_404_NOT_FOUND,
        )
