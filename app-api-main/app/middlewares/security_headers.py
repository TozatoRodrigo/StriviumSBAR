"""Security response headers middleware.

Adds a baseline set of hardening headers to every HTTP response to mitigate
common web risks (OWASP A05 - Security Misconfiguration):

- ``X-Content-Type-Options: nosniff`` - block MIME sniffing.
- ``X-Frame-Options`` / CSP ``frame-ancestors`` - clickjacking protection.
- ``Referrer-Policy`` - avoid leaking URLs to third parties.
- ``X-Permitted-Cross-Domain-Policies: none`` - block Adobe cross-domain access.
- ``Content-Security-Policy`` - restrictive default for API responses.
- ``Strict-Transport-Security`` - force HTTPS (opt-in, production only).

All behaviour is driven by ``app.core.environment`` so it can be tuned per
environment without code changes. Headers are added with ``setdefault`` so a
handler that intentionally sets its own value is never overridden.
"""

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.environment import envs

# Swagger UI / ReDoc need to load scripts and styles, so the strict
# ``default-src 'none'`` CSP must not be applied to the docs routes.
_CSP_EXEMPT_PREFIXES = ("/docs", "/redoc", "/openapi.json")


def _static_security_headers() -> dict[str, str]:
    """Build the headers that do not depend on the request path.

    Returns:
        Mapping of header name to value for the configured security headers.

    """
    headers = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": envs.SECURITY_FRAME_OPTIONS,
        "Referrer-Policy": envs.SECURITY_REFERRER_POLICY,
        "X-Permitted-Cross-Domain-Policies": "none",
    }
    if envs.SECURITY_HSTS_ENABLED:
        headers["Strict-Transport-Security"] = (
            f"max-age={envs.SECURITY_HSTS_MAX_AGE}; includeSubDomains"
        )
    return headers


class SecurityHeadersMiddleware:
    """Inject security headers into every HTTP response."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or not envs.SECURITY_HEADERS_ENABLED:
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")
        apply_csp = bool(envs.SECURITY_CSP) and not path.startswith(
            _CSP_EXEMPT_PREFIXES
        )

        async def send_with_security_headers(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                for key, value in _static_security_headers().items():
                    headers.setdefault(key, value)
                if apply_csp:
                    headers.setdefault("Content-Security-Policy", envs.SECURITY_CSP)
            await send(message)

        await self.app(scope, receive, send_with_security_headers)
