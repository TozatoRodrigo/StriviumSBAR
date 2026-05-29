import logging
from typing import Annotated
from uuid import UUID

from fastapi import Body, Depends, status
from fastapi.responses import JSONResponse
from jose import JWTError
from jose import jwt as jose_jwt

from app.core.environment import envs
from app.modules.auth.di.use_cases import (
    get_refresh_tenant_auth_use_case,
    get_refresh_token_service,
    get_refresh_user_auth_use_case,
)
from app.modules.auth.services.refresh_token.refresh_token_service import (
    RefreshTokenService,
)
from app.modules.auth.use_cases.refresh_auth.refresh_tenant_auth_use_case import (
    RefreshTenantAuthUseCase,
)
from app.modules.auth.use_cases.refresh_auth.refresh_user_auth_use_case import (
    RefreshUserAuthUseCase,
)

log = logging.getLogger("logger")


def refresh_user_auth(
    refresh_token: Annotated[str, Body(embed=True)],
    refresh_user_auth_use_case: Annotated[
        RefreshUserAuthUseCase, Depends(get_refresh_user_auth_use_case)
    ],
) -> JSONResponse:
    auth_data = refresh_user_auth_use_case.handle(refresh_token)
    return JSONResponse(auth_data.to_json(), status_code=status.HTTP_200_OK)


def refresh_tenant_auth(
    refresh_token: Annotated[str, Body(embed=True)],
    refresh_tenant_auth_use_case: Annotated[
        RefreshTenantAuthUseCase, Depends(get_refresh_tenant_auth_use_case)
    ],
) -> JSONResponse:
    auth_data = refresh_tenant_auth_use_case.handle(refresh_token)
    return JSONResponse(auth_data.to_json(), status_code=status.HTTP_200_OK)


def logout(
    refresh_token: Annotated[str, Body(embed=True)],
    refresh_token_service: Annotated[
        RefreshTokenService, Depends(get_refresh_token_service)
    ],
) -> JSONResponse:
    try:
        payload = jose_jwt.decode(refresh_token, envs.JWT_SECRET, algorithms=["HS256"])
    except JWTError:
        log.info(
            "Logout received invalid refresh token",
            extra={"event": "auth.logout.invalid_refresh"},
        )
        return JSONResponse(None, status_code=status.HTTP_204_NO_CONTENT)

    jti_claim = payload.get("jti")
    if not jti_claim:
        log.info(
            "Logout refresh token without jti",
            extra={"event": "auth.logout.missing_jti"},
        )
        return JSONResponse(None, status_code=status.HTTP_204_NO_CONTENT)

    try:
        refresh_token_service.revoke_by_jti(UUID(jti_claim))
    except ValueError:
        log.info(
            "Logout refresh token with malformed jti",
            extra={"event": "auth.logout.invalid_jti"},
        )
    except Exception:
        log.exception(
            "Failed to revoke refresh token during logout",
            extra={"event": "auth.logout.revoke_failed"},
        )

    return JSONResponse(None, status_code=status.HTTP_204_NO_CONTENT)
