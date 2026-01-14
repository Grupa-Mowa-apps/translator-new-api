import logging
from app.domain.ports.file_repository import FileRepository
from app.domain.errors import FileErrors
from app.domain.ports.file_storage import FileStorage

logger = logging.getLogger(__name__)

class DeleteFileCommand:
    def __init__(self, repo: FileRepository, storage: FileStorage):
        self.repo = repo
        self.storage = storage

    def run(self, file_id: str) -> None:
        file = self.repo.get(file_id)
        if not file:
            raise ValueError(FileErrors.FILE_NOT_FOUND)

        self.storage.delete(file.path)

        ok = self.repo.delete(file_id)
        if not ok:
            raise ValueError(FileErrors.FILE_NOT_FOUND)