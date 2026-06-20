from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from .core.environment import envs
from .core.rate_limiter import limiter
from .exceptions.client_aware_error import ClientAwareError
from .exceptions.handler import (
    client_aware_error_handler,
    exception_handler,
    http_exception_handler,
)
from .middlewares.set_timezone import SetTimezoneMiddleware
from .routes import router

JWT_SECRET_MIN_LENGTH = 32


def rate_limit_exceeded_handler(
    request: Request, exc: RateLimitExceeded
) -> JSONResponse:
    """Handle rate limit exceeded errors with a JSON response.

    Args:
        request: The incoming request that exceeded the rate limit.
        exc: The rate limit exceeded exception.

    Returns:
        JSONResponse with 429 status code and error message.

    """
    return JSONResponse(
        status_code=429,
        content={"error": f"Rate limit exceeded: {exc.detail}"},
    )


def _ensure_security_configuration() -> None:
    secret = envs.JWT_SECRET.strip()
    if len(secret) < JWT_SECRET_MIN_LENGTH:
        msg = f"JWT_SECRET must contain at least {JWT_SECRET_MIN_LENGTH} characters"
        raise RuntimeError(msg)


_ensure_security_configuration()

cors_allowed_origins = [
    origin.strip() for origin in envs.CORS_ALLOWED_ORIGINS.split(",") if origin.strip()
]
if not cors_allowed_origins:
    cors_allowed_origins = [envs.APP_URL]

app = FastAPI(
    title="Strivium API",
    description="API para o sistema Strivium",
    version="1.0.0",
    docs_url="/docs" if envs.ENABLE_DOCS else None,
    redoc_url="/redoc" if envs.ENABLE_DOCS else None,
    openapi_url="/openapi.json" if envs.ENABLE_DOCS else None,
)
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SetTimezoneMiddleware)
app.add_middleware(SlowAPIMiddleware)


add_pagination(app)

app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(ClientAwareError, client_aware_error_handler)
app.add_exception_handler(Exception, exception_handler)

app.include_router(router)

if envs.FILESYSTEM_DRIVER == "local":
    storage_path = Path("storage", "static")
    app.mount("/static", StaticFiles(directory=storage_path), name="static")
