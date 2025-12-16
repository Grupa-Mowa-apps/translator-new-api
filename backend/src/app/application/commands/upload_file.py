import uuid
import logging
from app.domain.ports.file_repository import FileRepository
from app.application.dto.file_dto import FileResponse, UploadFileRequest
from app.domain.entities.file import File
from app.domain.errors import FileErrors

logger = logging.getLogger(__name__)

class UploadFileCommand:
    def __init__(self, repo: FileRepository):
        self.repo = repo

    def run(self, dto: UploadFileRequest) -> FileResponse:
        if not dto.owner_id or not dto.owner_id.strip():
            raise ValueError(FileErrors.OWNER_ID_CANNOT_BE_EMPTY)
        if not dto.filename or not dto.filename.strip():
            raise ValueError(FileErrors.FILENAME_CANNOT_BE_EMPTY)
        
        file_id = uuid.uuid4().hex
        file_path = f"{file_id}/{dto.filename}/{dto.kind}"

        file = File(
            id=file_id,
            owner_id=dto.owner_id, 
            kind=dto.kind,
            path=file_path,
            filename=dto.filename,
            book_id=dto.book_id
        )
        self.repo.add(file)
        self.repo.session.commit()
        logger.info(f"File uploaded: {file.id} - {file.filename}")
        
        return FileResponse(
            id=file.id,
            owner_id=file.owner_id,
            kind=file.kind,
            path=file.path,
            filename=file.filename,
            book_id=file.book_id,
            version=file.version
        )