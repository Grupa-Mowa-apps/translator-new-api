import uuid
from app.domain.ports.file_repository import FileRepository
from app.application.dto.file_dto import FileResponse, UploadFileRequest
from app.domain.entities.file import File


class UploadFileCommand:
    def __init__(self, repo: FileRepository):
        self.repo = repo

    def run(self, dto: UploadFileRequest) -> FileResponse:
        file_id = uuid.uuid4().hex
        file_path = f"{file_id}/{dto.filename}/{dto.kind}"

        file = File(
            id=uuid.uuid4().hex, owner_id=dto.owner_id, 
            kind=dto.kind, path=file_path, filename=dto.filename,
            book_id=dto.book_id
        )
        self.repo.add(file)
        return FileResponse(
            id=file.id,
            owner_id=file.owner_id,
            kind=file.kind,
            path=file.path,
            filename=file.filename,
            book_id=file.book_id,
            version=file.version
        )