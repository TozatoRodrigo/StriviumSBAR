"""Rate limiter configuration for the Strivium API.

This module provides a centralized rate limiter instance used across the
application to throttle requests and protect endpoints against abuse and
brute-force attacks (OWASP API4:2023 - Unrestricted Resource Consumption).

All behaviour is driven by environment variables (see ``app.core.environment``):

- ``RATE_LIMIT_ENABLED``: master switch (disabled automatically in tests).
- ``RATE_LIMIT_STORAGE_URI``: ``memory://`` for a single instance, or a Redis
  URL (e.g. ``redis://strivium-redis:6379/0``) for distributed rate limiting
  shared across multiple API instances.
- ``RATE_LIMIT_DEFAULT``: global limits applied to every endpoint, as a
  ``;``-separated list (e.g. ``100/minute;1000/hour``).
- ``RATE_LIMIT_AUTH_LOGIN`` / ``RATE_LIMIT_AUTH_TENANT``: stricter limits for
  sensitive authentication endpoints.

Usage in routes::

    from fastapi import Request
    from app.core.rate_limiter import limiter

    @router.get("/endpoint")
    @limiter.limit("10/minute")
    async def endpoint(request: Request) -> ...:
        ...

The ``request: Request`` parameter is required by SlowAPI on any decorated
route handler.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.environment import envs


def _parse_limits(raw: str) -> list[str]:
    """Split a ``;``-separated limit string into a list of SlowAPI limits.

    Returns:
        The non-empty, whitespace-trimmed limit expressions (e.g.
        ``["100/minute", "1000/hour"]``).

    """
    return [limit.strip() for limit in raw.split(";") if limit.strip()]


# Centralized, env-driven limit definitions so callers reference a single
# source of truth instead of hardcoding limit strings at each call site.
DEFAULT_LIMITS = _parse_limits(envs.RATE_LIMIT_DEFAULT)
AUTH_LOGIN_LIMIT = envs.RATE_LIMIT_AUTH_LOGIN
AUTH_TENANT_LIMIT = envs.RATE_LIMIT_AUTH_TENANT

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=DEFAULT_LIMITS,
    storage_uri=envs.RATE_LIMIT_STORAGE_URI,
    enabled=envs.RATE_LIMIT_ENABLED,
    # Emit X-RateLimit-Limit / X-RateLimit-Remaining / X-RateLimit-Reset and
    # Retry-After headers so clients can self-throttle.
    headers_enabled=True,
)
