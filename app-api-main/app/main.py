from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from slowapi import _rate_limit_exceeded_handler
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
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(SetTimezoneMiddleware)


add_pagination(app)

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(ClientAwareError, client_aware_error_handler)
app.add_exception_handler(Exception, exception_handler)

app.include_router(router)

if envs.FILESYSTEM_DRIVER == "local":
    storage_path = Path("storage", "static")
    app.mount("/static", StaticFiles(directory=storage_path), name="static")
