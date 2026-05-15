from fastapi import status

from app.exceptions.client_aware_error import ClientAwareError


class DoctorAlreadyExistsError(ClientAwareError):
    EMAIL_MESSAGE = "Já existe um médico com este e-mail"
    DOCUMENT_MESSAGE = "Já existe um médico com este CPF"
    CRM_MESSAGE = "Já existe um médico com este CRM"

    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def for_email(cls) -> "DoctorAlreadyExistsError":
        return cls(cls.EMAIL_MESSAGE)

    @classmethod
    def for_document(cls) -> "DoctorAlreadyExistsError":
        return cls(cls.DOCUMENT_MESSAGE)

    @classmethod
    def for_crm(cls) -> "DoctorAlreadyExistsError":
        return cls(cls.CRM_MESSAGE)
