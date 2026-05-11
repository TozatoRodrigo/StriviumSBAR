from .filesystem_adapter import FilesystemAdapter


class FakeFilesystemAdapter(FilesystemAdapter):
    def url(self, path: str) -> str:  # noqa: PLR6301
        return f"fake://{path}"

    def signed_url(self, path: str) -> str:  # noqa: PLR6301
        return f"fake://{path}"

    def put(self, path: str, content: bytes) -> None:
        pass

    def get(self, path: str) -> bytes:
        pass

    def delete(self, path: str) -> None:
        pass
