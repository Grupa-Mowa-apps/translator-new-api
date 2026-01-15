from typing import Optional
from app.domain.ports.file_repository import FileRepository
from app.application.dto.file_dto import FileResponse
from app.domain.errors import FileErrors


class GetFileQuery:
    def __init__(self, repo: FileRepository):
        self.repo = repo

    def execute(self, file_id: str) -> Optional[FileResponse]:
        file = self.repo.get(file_id)
        if not file:
            raise ValueError(FileErrors.FILE_NOT_FOUND)
        return FileResponse(
            id=file.id,
            owner_id=file.owner_id,
            kind=file.kind,
            path=file.path,
            filename=file.filename,
            book_id=file.book_id,
            version=file.version
        )