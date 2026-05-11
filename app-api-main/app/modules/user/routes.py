from fastapi import APIRouter, Depends, status

from app.dtos.exception.exception_dto import ExceptionDTO
from app.middlewares.auth_middleware import verify_user_jwt
from app.middlewares.turnstile_middleware import verify_turnstile_token
from app.modules.user.controllers.user_controller import create_user, get_user_info
from app.modules.user.dtos.responses.user.user_response import (
    UserResponseDTO,
)

router = APIRouter(prefix="/user/v1", tags=["user"])


router.add_api_route(
    "/users",
    create_user,
    methods=["POST"],
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseDTO,
    dependencies=[Depends(verify_turnstile_token)],
    responses={
        status.HTTP_201_CREATED: {"model": UserResponseDTO},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionDTO},
    },
)

router.add_api_route(
    "/users/info",
    get_user_info,
    methods=["GET"],
    dependencies=[Depends(verify_user_jwt)],
    summary="Get authenticated user info",
    responses={
        status.HTTP_200_OK: {"model": UserResponseDTO},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionDTO},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionDTO},
    },
)
