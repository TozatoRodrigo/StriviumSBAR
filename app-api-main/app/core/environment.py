import os
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.testing" if os.getenv("APP_ENV") == "testing" else ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

    APP_URL: str = "http://localhost:55000"

    JWT_SECRET: str = ""

    DB_DRIVER: str = "postgresql"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_DEBUG: bool = False

    ENABLE_DOCS: bool = False

    APP_MODULE: str | None = None

    FILESYSTEM_DRIVER: str = "local"

    GCS_BASE_URL: str | None = None
    GCS_PROJECT_ID: str | None = None
    GCS_BUCKET_NAME: str | None = None
    GCS_KEY_FILE: str | None = None

    S3_PUBLIC_URL: str | None = None
    S3_BUCKET_NAME: str | None = None
    S3_ENDPOINT_URL: str | None = None
    S3_AWS_ACCESS_KEY_ID: str | None = None
    S3_AWS_SECRET_ACCESS_KEY: str | None = None

    MAIL_HOST: str | None = None
    MAIL_PORT: int | None = None
    MAIL_USERNAME: str | None = None
    MAIL_PASSWORD: str | None = None
    MAIL_FROM: str | None = None
    MAIL_USE_TLS: bool = True

    TURNSTILE_ENABLED: bool = True
    CLOUDFLARE_TURNSTILE_SECRET: str = ""

    SBAR_AI_ENABLED: bool = False
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2:3b"
    OLLAMA_TIMEOUT_SECONDS: float = 30


envs = Environment()


def get_env(name: str, default: Any | None = None) -> Any:
    return getattr(envs, name, default)
