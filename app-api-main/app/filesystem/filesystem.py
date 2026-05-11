from app.config import filesystem
from app.filesystem.adapters.fake_filesystem_adapter import FakeFilesystemAdapter
from app.filesystem.adapters.filesystem_adapter import FilesystemAdapter

if filesystem.driver == "local":
    from app.filesystem.adapters.local_filesystem_adapter import (
        LocalFilesystemAdapter,
    )
elif filesystem.driver == "gcs":
    from app.filesystem.adapters.google_filesystem_adapter import (
        GoogleFilesystemAdapter,
    )

elif filesystem.driver == "s3":
    from app.filesystem.adapters.s3_filesystem_adapter import (
        S3FilesystemAdapter,
    )


class Filesystem:
    def __init__(self) -> None:
        self.driver = filesystem.driver
        self.config = filesystem.configs[self.driver]
        self.adapter = self.get_adapter()

    def get_adapter(self) -> FilesystemAdapter:
        if self.driver == "local":
            return LocalFilesystemAdapter(self.config)
        if self.driver == "gcs":
            return GoogleFilesystemAdapter(self.config)
        if self.driver == "s3":
            return S3FilesystemAdapter(self.config)
        if self.driver == "fake":
            return FakeFilesystemAdapter(self.config)
        msg = f"Invalid driver: {self.driver}"
        raise ValueError(msg)

    def url(self, path: str) -> str:
        return self.adapter.url(path)

    def signed_url(self, path: str) -> str:
        return self.adapter.signed_url(path)

    def put(self, path: str, content: bytes) -> None:
        return self.adapter.put(path, content)

    def get(self, path: str) -> bytes:
        return self.adapter.get(path)

    def delete(self, path: str) -> None:
        return self.adapter.delete(path)
