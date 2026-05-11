from typing import Annotated

from fastapi import Depends

from app.di.services import get_user_token_service
from app.modules.user.di.mappers import get_user_mapper
from app.modules.user.di.repositories import get_user_repository
from app.modules.user.interfaces.repositories.user_repository import UserRepository
from app.modules.user.mappers.user_mapper import UserMapper
from app.modules.user.use_cases.user.create_user_use_case import CreateUserUseCase
from app.modules.user.use_cases.user.fetch_user_info_use_case import (
    FetchUserInfoUseCase,
)
from app.services.token.user_token_service import UserTokenService


def get_create_user_use_case(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    user_mapper: Annotated[UserMapper, Depends(get_user_mapper)],
) -> CreateUserUseCase:
    return CreateUserUseCase(user_repository, user_mapper)


def get_fetch_user_info_use_case(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    user_mapper: Annotated[UserMapper, Depends(get_user_mapper)],
    token_service: Annotated[UserTokenService, Depends(get_user_token_service)],
) -> FetchUserInfoUseCase:
    return FetchUserInfoUseCase(token_service, user_repository, user_mapper)
