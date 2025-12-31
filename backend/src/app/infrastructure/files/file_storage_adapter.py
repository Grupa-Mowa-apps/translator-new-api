import os
from pathlib import Path
import re
from uuid import uuid4

from app.domain.ports.file_storage import FileStorage
from app.domain.errors import FileErrors


_FILENAME_SAFE_RE = re.compile(r"[^A-Za-z0-9._-]+")

def _sanitize_filename(name: str) -> str:
    name = (name or "file").strip()
    name = name.replace("\\", "_").replace("/", "_")
    name = _FILENAME_SAFE_RE.sub("_", name)
    return name[:200] or "file"

class FileStorageAdapter(FileStorage):
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def save(
        self, 
        owner_id: str, 
        filename: str, 
        content: bytes, 
        content_type: str | None = None
    ) -> str:
        
        clean_filename = _sanitize_filename(filename)
        extension = Path(clean_filename).suffix

        owner_dir = self.base_dir / owner_id
        owner_dir.mkdir(parents=True, exist_ok=True)

        unique_name = f"{uuid4().hex}{extension}" if extension else uuid4().hex
        relative_path = Path(owner_id) / unique_name
        absolute_path = (self.base_dir / relative_path).resolve()

        absolute_path.write_bytes(content)
        return str(relative_path).replace(os.sep, "/")
    
    def delete(self, storage_path: str) -> None:
        if not storage_path:
            return

        relative_path = Path(storage_path)
        base = self.base_dir.resolve()
        absolute_path = (self.base_dir / relative_path).resolve()

        if base not in absolute_path.parents and absolute_path != base:
            raise ValueError(FileErrors.INVALID_STORAGE_PATH)

        if absolute_path.exists():
            absolute_path.unlink()