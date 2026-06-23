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
    CORS_ALLOWED_ORIGINS: str = ""

    JWT_SECRET: str = ""
    REFRESH_TOKEN_STRICT_MODE: bool = True

    # Rate limiting. Defaults are safe for single-instance/local usage.
    # In production set RATE_LIMIT_STORAGE_URI to a Redis URL (e.g.
    # "redis://strivium-redis:6379/0") so limits are shared across instances.
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_STORAGE_URI: str = "memory://"
    RATE_LIMIT_DEFAULT: str = "100/minute;1000/hour"
    RATE_LIMIT_AUTH_LOGIN: str = "5/minute"
    RATE_LIMIT_AUTH_TENANT: str = "10/minute"

    # Security response headers (OWASP A05 - Security Misconfiguration).
    # HSTS is disabled by default because it only makes sense over HTTPS;
    # enable it in production (behind TLS).
    SECURITY_HEADERS_ENABLED: bool = True
    SECURITY_HSTS_ENABLED: bool = False
    SECURITY_HSTS_MAX_AGE: int = 63072000
    SECURITY_CSP: str = "default-src 'none'; frame-ancestors 'none'; base-uri 'none'"
    SECURITY_REFERRER_POLICY: str = "no-referrer"
    SECURITY_FRAME_OPTIONS: str = "DENY"

    # Audit logging (LGPD Art. 46/48). Retention defaults to 180 days (~6 months),
    # the minimum recommended for traceability of access to personal data.
    AUDIT_LOG_ENABLED: bool = True
    AUDIT_LOG_RETENTION_DAYS: int = 180

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
    UPLOAD_MAX_FILE_SIZE_MB: int = 20
    UPLOAD_ALLOWED_EXTENSIONS: str = "png,jpg,jpeg,webp,pdf,mp3,wav,m4a,mp4,mov"
    UPLOAD_ALLOWED_MIME_TYPES: str = (
        "image/png,image/jpeg,image/webp,application/pdf,audio/mpeg,audio/wav,"
        "audio/x-wav,audio/mp4,audio/x-m4a,video/mp4,video/quicktime"
    )

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
    TENANT_INVITE_EMAIL_ENABLED: bool = False

    TURNSTILE_ENABLED: bool = True
    CLOUDFLARE_TURNSTILE_SECRET: str = ""

    SBAR_AI_ENABLED: bool = False
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2:3b"
    OLLAMA_TIMEOUT_SECONDS: float = 30


envs = Environment()


def get_env(name: str, default: Any | None = None) -> Any:
    return getattr(envs, name, default)
