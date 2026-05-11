from app.exceptions.client_aware_error import ClientAwareError


class AuthError(ClientAwareError):
    def __init__(self, message: str = "Credenciais Inválidas") -> None:
        super().__init__(message, 401)
