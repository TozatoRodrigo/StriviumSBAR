"""Tests for the security response headers middleware (OWASP A05)."""

from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from app.main import app as production_app
from app.middlewares.security_headers import SecurityHeadersMiddleware


def _build_app() -> FastAPI:
    """Build a minimal app guarded by the security headers middleware.

    Returns:
        A FastAPI app exposing ``/ping`` and a fake ``/docs`` route.

    """
    app = FastAPI()
    app.add_middleware(SecurityHeadersMiddleware)

    @app.get("/ping")
    async def ping() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/docs")
    async def docs() -> dict[str, str]:
        return {"status": "docs"}

    return app


def test_baseline_security_headers_present() -> None:
    """Every response carries the baseline hardening headers."""
    client = TestClient(_build_app())

    response = client.get("/ping")

    assert response.status_code == status.HTTP_200_OK
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert response.headers["X-Permitted-Cross-Domain-Policies"] == "none"
    assert "Content-Security-Policy" in response.headers


def test_csp_skipped_for_docs_routes() -> None:
    """Swagger/ReDoc routes keep the baseline headers but no strict CSP."""
    client = TestClient(_build_app())

    response = client.get("/docs")

    assert response.status_code == status.HTTP_200_OK
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert "Content-Security-Policy" not in response.headers


def test_production_app_sets_security_headers() -> None:
    """The wired production app applies the middleware end to end."""
    client = TestClient(production_app)
    response = client.get("/health")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
