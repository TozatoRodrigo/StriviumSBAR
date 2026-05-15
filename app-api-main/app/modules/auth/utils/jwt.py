from datetime import UTC, datetime, timedelta
from uuid import UUID

from jose import jwt

from app.core.environment import envs

ACCESS_TOKEN_TYPE = "Bearer"  # noqa: S105
ACCESS_TOKEN_EXPIRES_MINUTES = 60 * 2
REFRESH_TOKEN_EXPIRES_MINUTES = 60 * 24 * 30


def generate_access_token(subject: dict) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)

    payload = {"exp": expire, **subject}
    return jwt.encode(payload, envs.JWT_SECRET, algorithm="HS256")


def generate_refresh_token(subject: dict, jti: UUID | None = None) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=REFRESH_TOKEN_EXPIRES_MINUTES)

    payload = {"exp": expire, **subject}
    if jti is not None:
        payload["jti"] = str(jti)
    return jwt.encode(payload, envs.JWT_SECRET, algorithm="HS256")
