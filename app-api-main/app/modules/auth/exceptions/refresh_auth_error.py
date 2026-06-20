from app.exceptions.client_aware_error import ClientAwareError


class RefreshAuthError(ClientAwareError):
    def __init__(
        self, message: str = "Erro ao realizar refresh de autenticação"
    ) -> None:
        super().__init__(message, 400)
