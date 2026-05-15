from app.exceptions.client_aware_error import ClientAwareError


class AuthorizationError(ClientAwareError):
    def __init__(self, message: str = "Acesso negado") -> None:
        super().__init__(message, 403)
