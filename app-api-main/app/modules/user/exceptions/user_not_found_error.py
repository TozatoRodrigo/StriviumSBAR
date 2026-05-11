from app.exceptions.client_aware_error import ClientAwareError


class UserNotFoundError(ClientAwareError):
    def __init__(self, message: str) -> None:
        super().__init__(message, 404)
