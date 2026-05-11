from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from app.core.environment import envs
from app.core.logging import logger
from app.di.services import get_turnstile_service
from app.services.cloudflare.turnstile import TurnstileService


async def verify_turnstile_token(
    request: Request,
    turnstile_service: Annotated[TurnstileService, Depends(get_turnstile_service)],
) -> None:
    if not envs.TURNSTILE_ENABLED:
        logger.info("Turnstile validation skipped (TURNSTILE_ENABLED=false)")
        return

    x_turnstile_token = request.headers.get("x-turnstile-token")

    if not x_turnstile_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Turnstile token in header",
        )

    client_ip = request.client.host if request.client else None

    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()
    else:
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            client_ip = real_ip

    validation = await turnstile_service.validate(
        x_turnstile_token,
        envs.CLOUDFLARE_TURNSTILE_SECRET,
        client_ip,
    )

    if not validation.get("success"):
        logger.info("Invalid cloudflare turnstile token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Turnstile token",
        )

    logger.info("Turnstile token validado com sucesso")
