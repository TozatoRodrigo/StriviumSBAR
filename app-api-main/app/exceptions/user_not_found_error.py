from app.exceptions.client_aware_error import ClientAwareError


class UserNotFoundError(ClientAwareError):
    def __init__(self) -> None:
        super().__init__("Usuário não encontrado", 404)
