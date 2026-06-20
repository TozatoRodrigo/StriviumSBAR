from app.utils.url import build_url

from .filesystem_adapter import FilesystemAdapter


class GoogleFilesystemAdapter(FilesystemAdapter):
    def url(self, path: str) -> str:
        return build_url(self.config["base_url"], path)

    def signed_url(self, path: str) -> str:
        return build_url(self.config["base_url"], path)

    def put(self, path: str, content: bytes) -> None:
        pass

    def get(self, path: str) -> bytes:
        pass

    def delete(self, path: str) -> None:
        pass
