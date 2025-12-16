import logging
from app.domain.ports.file_repository import FileRepository
from app.domain.errors import FileErrors

logger = logging.getLogger(__name__)

class DeleteFileCommand:
    def __init__(self, repo: FileRepository):
        self.repo = repo

    def run(self, file_id: str) -> None:
        file = self.repo.get(file_id)
        if not file:
            raise ValueError(FileErrors.FILE_NOT_FOUND)
        self.repo.delete(file_id)
        self.repo.session.commit()
        logger.info(f"File deleted: {file_id}")