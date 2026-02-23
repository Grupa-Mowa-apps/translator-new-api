import os
from pathlib import Path
import logging
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    log.error("Missing env var: DATABASE_URL")
    raise RuntimeError("Missing env var: DATABASE_URL")

LLM_MODEL = "gpt-4o-mini"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

FILE_STORAGE_DIR = Path(os.getenv("FILE_STORAGE_DIR", "/app/backend/storage")).resolve()