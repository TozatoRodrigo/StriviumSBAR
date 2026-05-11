import os
from collections.abc import Generator
from pathlib import Path

from sqlmodel import Session as SQLModelSession
from sqlmodel import create_engine

from .environment import envs

if os.getenv("APP_ENV") == "testing":
    test_db_path = Path("test.sqlite")
    DATABASE_URL = f"sqlite:///{test_db_path}"
    engine = create_engine(
        DATABASE_URL,
        echo=envs.DB_DEBUG,
        connect_args={"check_same_thread": False},
    )
else:
    DATABASE_URL = f"{envs.DB_DRIVER}://{envs.DB_USER}:{envs.DB_PASSWORD}@{envs.DB_HOST}:{envs.DB_PORT}/{envs.DB_NAME}"
    engine = create_engine(
        DATABASE_URL,
        echo=envs.DB_DEBUG,
    )


def get_session() -> Generator[SQLModelSession]:
    with SQLModelSession(engine) as session:
        yield session
