"""Tests for API rate limiting.

These tests are split in two parts:

1. Configuration tests assert that the production app is correctly wired with
   the SlowAPI limiter, exception handler and middleware.
2. A behavioural test builds an isolated app with an *enabled* limiter so the
   throttling logic can be verified deterministically, without depending on
   ``RATE_LIMIT_ENABLED`` (which is disabled in the test environment to avoid
   throttling unrelated suites).
"""

from fastapi import FastAPI, Request, Response, status
from fastapi.testclient import TestClient
from slowapi import Limiter, _rate_limit_exceeded_handler  # noqa: PLC2701
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.core.rate_limiter import DEFAULT_LIMITS, limiter
from app.main import app

ALLOWED_REQUESTS = 3
ISOLATED_LIMIT = f"{ALLOWED_REQUESTS}/minute"


def test_limiter_is_registered_on_app() -> None:
    """The production app exposes the limiter on its state."""
    assert hasattr(app.state, "limiter"), "Rate limiter should be on app.state"
    assert app.state.limiter is limiter


def test_default_limits_are_parsed_from_configuration() -> None:
    """Global default limits are derived from RATE_LIMIT_DEFAULT."""
    assert DEFAULT_LIMITS, "At least one default limit should be configured"
    assert all("/" in limit for limit in DEFAULT_LIMITS)


def test_rate_limit_exceeded_handler_is_registered() -> None:
    """A 429 handler is registered so clients get a clean error response."""
    assert RateLimitExceeded in app.exception_handlers


def _build_isolated_app(limit: str) -> FastAPI:
    """Build a minimal app whose only route is throttled at ``limit``.

    Returns:
        A FastAPI app with a single ``GET /ping`` route guarded by an enabled
        limiter using in-memory storage.

    """
    isolated_limiter = Limiter(
        key_func=get_remote_address,
        enabled=True,
        headers_enabled=True,
        storage_uri="memory://",
    )
    isolated_app = FastAPI()
    isolated_app.state.limiter = isolated_limiter
    isolated_app.add_middleware(SlowAPIMiddleware)
    isolated_app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # SlowAPI injects the X-RateLimit-* headers into ``response`` when
    # ``headers_enabled`` is on, so the handler must declare that parameter.
    @isolated_app.get("/ping")
    @isolated_limiter.limit(limit)
    async def ping(request: Request, response: Response) -> dict[str, str]:
        return {"status": "ok"}

    return isolated_app


def test_requests_within_limit_are_allowed() -> None:
    """Requests below the threshold are served normally."""
    client = TestClient(_build_isolated_app(ISOLATED_LIMIT))

    for _ in range(ALLOWED_REQUESTS):
        response = client.get("/ping")
        assert response.status_code == status.HTTP_200_OK


def test_requests_over_limit_are_throttled() -> None:
    """Exceeding the threshold returns 429 with informative headers."""
    client = TestClient(_build_isolated_app(ISOLATED_LIMIT))

    statuses = [client.get("/ping").status_code for _ in range(ALLOWED_REQUESTS + 2)]

    assert statuses.count(status.HTTP_200_OK) == ALLOWED_REQUESTS
    assert status.HTTP_429_TOO_MANY_REQUESTS in statuses

    throttled = client.get("/ping")
    assert throttled.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert "X-RateLimit-Limit" in throttled.headers
    assert "Retry-After" in throttled.headers
