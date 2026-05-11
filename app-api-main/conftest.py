import sys
from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from sqlmodel import Session, SQLModel

from app.core.database import engine
from app.di.services import get_turnstile_service
from app.main import app
from app.seed import seed

sys.path.insert(0, str(Path(__file__).parent.absolute()))


@pytest.fixture(autouse=True)
def clean_tables() -> None:
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    seed()


@pytest.fixture(autouse=True)
def db_session() -> Generator[Session]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def mock_turnstile_validation() -> Generator[MagicMock]:
    mock_instance = MagicMock()

    async def mock_validate(*args, **kwargs):  # noqa: ANN002, ANN003, ANN202, RUF029
        return {"success": True}

    mock_instance.validate = mock_validate

    app.dependency_overrides.clear()

    app.dependency_overrides[get_turnstile_service] = lambda: mock_instance

    yield mock_instance

    app.dependency_overrides.clear()
