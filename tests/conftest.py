from pathlib import Path
import os, logging
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "backend" / "src"))

from dotenv import load_dotenv
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, clear_mappers
from app.infrastructure.db.models import Base

logger = logging.getLogger(__name__)

ENV_PATH = ROOT / "backend" / ".env"
loaded = load_dotenv(ENV_PATH, override=False)
if not loaded:
    logger.warning(f"Could not find or could not load .env file at {ENV_PATH}")

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
if not TEST_DATABASE_URL:
    raise pytest.UsageError("TEST_DATABASE_URL not found")

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        TEST_DATABASE_URL, 
        future=True,
        echo=False,
    )

    if TEST_DATABASE_URL.startswith("sqlite"):
        with engine.connect() as conn:
            conn.execute(text("PRAGMA foreign_keys=ON"))
    
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    try:
        yield engine
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()

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
        # clear_mappers()