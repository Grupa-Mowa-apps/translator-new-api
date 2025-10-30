from app.domain.ports.file_repository import FileRepository
from app.domain.errors import FileErrors


class DeleteFileCommand:
    def __init__(self, repo: FileRepository):
        self.repo = repo

    def run(self, file_id: str) -> None:
        if not self.repo.get(file_id):
            raise ValueError(FileErrors.FILE_NOT_FOUND)
        self.repo.delete(file_id)