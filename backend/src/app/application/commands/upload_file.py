import uuid
import logging
from app.domain.ports.file_repository import FileRepository
from app.application.dto.file_dto import FileResponse, UploadFileRequest
from app.domain.entities.file import File
from app.domain.ports.file_storage import FileStorage
from app.domain.value_objects.file_kind import FileKind

logger = logging.getLogger(__name__)

class UploadFileCommand:
    def __init__(self, repo: FileRepository, storage: FileStorage):
        self.repo = repo
        self.storage = storage

    def run(
        self,
        owner_id: str,
        kind: FileKind,
        filename: str,
        content: bytes,
        content_type: str | None = None,
        book_id: str | None = None,
    ) -> FileResponse:
        storage_path = self.storage.save(
            owner_id=owner_id,
            filename=filename,
            content=content,
            content_type=content_type,
        )

        file = File(
            id=uuid.uuid4().hex,
            owner_id=owner_id,
            kind=kind,
            path=storage_path,
            filename=filename,
            book_id=book_id,
        )
        self.repo.add(file)

        return FileResponse(
            id=file.id,
            owner_id=file.owner_id,
            kind=file.kind,
            path=file.path,
            filename=file.filename,
            book_id=file.book_id,
            version=file.version,
        )