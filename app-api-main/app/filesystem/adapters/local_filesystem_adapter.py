from pathlib import Path

import fsspec

from app.utils.url import build_url

from .filesystem_adapter import FilesystemAdapter

fs = fsspec.filesystem("file")


class LocalFilesystemAdapter(FilesystemAdapter):
    def url(self, path: str) -> str:
        dir_path = self.get_file_path(path)
        return build_url(self.config["base_url"], dir_path)

    def signed_url(self, path: str) -> str:
        dir_path = self.get_file_path(path)
        return build_url(self.config["base_url"], dir_path)

    def put(self, path: str, content: bytes) -> None:
        dir_path = self.get_full_path(path)
        with fs.open(dir_path, "wb") as f:
            f.write(content)

    def get(self, path: str) -> bytes:
        file_path = self.get_full_path(path)
        with fs.open(file_path, "rb") as f:
            return f.read()

    def delete(self, path: str) -> None:
        file_path = self.get_full_path(path)
        fs.rm(file_path)

    @staticmethod
    def get_file_path(path: str) -> str:
        path_parts = [part for part in path.split("/") if part]
        return "/static/" + "/".join(path_parts)

    @staticmethod
    def get_full_path(path: str) -> str:
        base_path = Path().cwd()
        path_parts = [part for part in path.split("/") if part]
        return str(base_path / "storage" / "static" / "/".join(path_parts))
