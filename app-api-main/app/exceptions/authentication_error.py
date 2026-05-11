from app.exceptions.client_aware_error import ClientAwareError


class AuthenticationError(ClientAwareError):
    def __init__(self, message: str = "Não autorizado") -> None:
        super().__init__(message, 401)
