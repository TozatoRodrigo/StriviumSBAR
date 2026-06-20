"""
Rate limiter configuration for the Strivium API.

This module provides a centralized rate limiter instance that can be used
across the application to apply rate limits to specific endpoints.

Default limits:
- 100 requests per minute
- 1000 requests per hour

Usage in routes:
    from app.core.rate_limiter import limiter

    @router.get("/endpoint")
    @limiter.limit("10/minute")
    async def endpoint(request: Request):
        ...
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

# Create limiter instance with default limits
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute", "1000/hour"],
    storage_uri="memory://",
)
