import os
from dotenv import load_dotenv

# wczyta .env z roota projektu (uruchamiaj z root)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("Missing env var: DATABASE_URL")
