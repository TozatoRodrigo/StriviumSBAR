from fastapi import status

from app.exceptions.client_aware_error import ClientAwareError


class UserAlreadyExistsError(ClientAwareError):
    EMAIL_MESSAGE = "Já existe um usuário com este e-mail"
    DOCUMENT_MESSAGE = "Já existe um usuário com este CPF"

    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def for_email(cls) -> "UserAlreadyExistsError":
        return cls(cls.EMAIL_MESSAGE)

    @classmethod
    def for_document(cls) -> "UserAlreadyExistsError":
        return cls(cls.DOCUMENT_MESSAGE)
