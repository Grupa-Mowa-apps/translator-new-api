import logging
from typing import Optional
from app.domain.ports.file_repository import FileRepository
from app.application.dto.file_dto import UpdateFileRequest, FileResponse
from app.domain.errors import FileErrors

logger = logging.getLogger(__name__)

class UpdateFileCommand:
    def __init__(self, repo: FileRepository):
        self.repo = repo

    def run(self, file_id: str, dto: UpdateFileRequest) -> Optional[FileResponse]:
        file = self.repo.get(file_id)
        if not file:
            raise ValueError(FileErrors.FILE_NOT_FOUND)
        if dto.owner_id:
            file.change_owner(dto.owner_id)
        if dto.kind:
            file.change_kind(dto.kind)
        if dto.filename:
            file.rename(dto.filename)
        self.repo.update(file)
        self.repo.session.commit()
        logger.info(f"File updated: {file.id}")
        
        return FileResponse(
            id=file.id,
            owner_id=file.owner_id,
            kind=file.kind,
            path=file.path,
            filename=file.filename,
            book_id=file.book_id,
            version=file.version
        ) 