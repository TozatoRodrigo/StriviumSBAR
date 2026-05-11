from app.exceptions.client_aware_error import ClientAwareError


class TenantNotFoundError(ClientAwareError):
    def __init__(self, message: str = "Workspace não encontrado") -> None:
        super().__init__(message, 404)
