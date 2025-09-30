from pathlib import Path
import os
from dotenv import load_dotenv
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, clear_mappers
from app.infrastructure.db.models import Base

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / "backend" / ".env"
load_dotenv(ENV_PATH, override=False)
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
print(TEST_DATABASE_URL)

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(TEST_DATABASE_URL, future=True)
    if TEST_DATABASE_URL.startswith("sqlite"):
        with engine.connect() as conn:
            conn.execute(text("PRAGMA foreign_keys=ON"))
        Base.metadata.create_all(engine)
        yield engine
        Base.metadata.drop_all(engine)
    else:
        Base.metadata.create_all(engine)
        yield engine
        Base.metadata.drop_all(engine)

@pytest.fixture()
def db_session(engine):
    connection = engine.connect()
    trans = connection.begin()
    Session = sessionmaker(
        bind=connection,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        future=True,
    )
    session = Session()
    try:
        yield session
    finally:
        session.close()
        trans.rollback()
        connection.close()
        clear_mappers()
