from typing import Annotated

from fastapi import Depends, status
from fastapi.responses import JSONResponse

from app.modules.user.di.use_cases import (
    get_create_user_use_case,
    get_fetch_user_info_use_case,
)
from app.modules.user.dtos.requests.user.create_user_request_dto import (
    CreateUserRequestDTO,
)
from app.modules.user.dtos.responses.user.user_response import UserResponseDTO
from app.modules.user.use_cases.user.create_user_use_case import CreateUserUseCase
from app.modules.user.use_cases.user.fetch_user_info_use_case import (
    FetchUserInfoUseCase,
)


def create_user(
    user_data: CreateUserRequestDTO,
    create_user_use_case: Annotated[
        CreateUserUseCase, Depends(get_create_user_use_case)
    ],
) -> JSONResponse:
    user = create_user_use_case.handle(user_data)
    return JSONResponse(user.to_json(), status_code=status.HTTP_201_CREATED)


def get_user_info(
    fetch_user_info_use_case: Annotated[
        FetchUserInfoUseCase, Depends(get_fetch_user_info_use_case)
    ],
) -> UserResponseDTO:
    user = fetch_user_info_use_case.handle()
    return JSONResponse(user.to_json(), status_code=status.HTTP_200_OK)
