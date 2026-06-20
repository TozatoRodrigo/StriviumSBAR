from typing import Annotated
from uuid import UUID

from fastapi import Header, HTTPException, Request, status
from jose import jwt

from app.core.environment import envs
from app.exceptions.tenant_not_found import TenantNotFoundError


def get_tenant_id_from_binding(request: Request) -> UUID:
    tenant_id = request.path_params["tenant_id"]
    if tenant_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurso não encontrado",
        )
    return UUID(tenant_id)


def get_tenant_id_from_token(
    authorization: Annotated[str, Header()],
) -> UUID:
    if not authorization:
        raise TenantNotFoundError

    authorization = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(authorization, envs.JWT_SECRET, algorithms=["HS256"])
        return UUID(payload["sub"])
    except Exception as e:
        raise TenantNotFoundError from e
