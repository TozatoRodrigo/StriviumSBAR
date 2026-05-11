from typing import Any

import boto3
from botocore.config import Config

from app.utils.url import build_url

from .filesystem_adapter import FilesystemAdapter


class S3FilesystemAdapter(FilesystemAdapter):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.s3 = boto3.client(
            "s3",
            endpoint_url=config["endpoint_url"],
            aws_access_key_id=config["aws_access_key_id"],
            aws_secret_access_key=config["aws_secret_access_key"],
            config=Config(signature_version="s3v4"),
        )

    def url(self, path: str) -> str:
        return build_url(self.config["public_url"], path)

    def signed_url(self, path: str) -> str:
        return self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.config["bucket_name"], "Key": path},
            ExpiresIn=3600,
        )

    def put(self, path: str, content: bytes) -> None:
        self.s3.put_object(Body=content, Bucket=self.config["bucket_name"], Key=path)

    def get(self, path: str) -> bytes:
        return self.s3.get_object(Bucket=self.config["bucket_name"], Key=path)[
            "Body"
        ].read()

    def delete(self, path: str) -> None:
        self.s3.delete_object(Bucket=self.config["bucket_name"], Key=path)
