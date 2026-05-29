from fastapi import status

from app.exceptions.client_aware_error import ClientAwareError
from app.utils.url import build_url

from .filesystem_adapter import FilesystemAdapter

GCS_NOT_IMPLEMENTED_MESSAGE = "Google Cloud Storage adapter is not yet implemented"


class GoogleFilesystemAdapter(FilesystemAdapter):
    def url(self, path: str) -> str:
        return build_url(self.config["base_url"], path)

    def signed_url(self, path: str) -> str:
        return build_url(self.config["base_url"], path)

    def put(self, _path: str, _content: bytes) -> None:  # noqa: PLR6301
        message = GCS_NOT_IMPLEMENTED_MESSAGE
        raise ClientAwareError(message, status.HTTP_501_NOT_IMPLEMENTED)

    def get(self, _path: str) -> bytes:  # noqa: PLR6301
        message = GCS_NOT_IMPLEMENTED_MESSAGE
        raise ClientAwareError(message, status.HTTP_501_NOT_IMPLEMENTED)

    def delete(self, _path: str) -> None:  # noqa: PLR6301
        message = GCS_NOT_IMPLEMENTED_MESSAGE
        raise ClientAwareError(message, status.HTTP_501_NOT_IMPLEMENTED)
