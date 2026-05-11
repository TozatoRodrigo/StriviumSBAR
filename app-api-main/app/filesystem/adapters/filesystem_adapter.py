from abc import ABC, abstractmethod
from typing import Any


class FilesystemAdapter(ABC):
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    @abstractmethod
    def url(self, path: str) -> str:
        pass

    @abstractmethod
    def signed_url(self, path: str) -> str:
        pass

    @abstractmethod
    def put(self, path: str, content: bytes) -> None:
        pass

    @abstractmethod
    def get(self, path: str) -> bytes:
        pass

    @abstractmethod
    def delete(self, path: str) -> None:
        pass
