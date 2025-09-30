import os
import logging
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    log.error("Missing env var: DATABASE_URL")
    raise RuntimeError("Missing env var: DATABASE_URL")
