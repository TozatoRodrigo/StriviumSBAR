from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.core.database import get_session
from app.modules.user.repositories.sqlmodel_user_repository import (
    SqlModelUserRepository,
    UserRepository,
)


def get_user_repository(
    session: Annotated[Session, Depends(get_session)],
) -> UserRepository:
    return SqlModelUserRepository(session)
