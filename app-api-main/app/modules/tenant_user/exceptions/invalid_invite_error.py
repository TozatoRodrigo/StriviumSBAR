from app.exceptions.client_aware_error import ClientAwareError


class InvalidInviteError(ClientAwareError):
    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=400)
