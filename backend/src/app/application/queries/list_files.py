from typing import List, Optional
from app.domain.ports.file_repository import FileRepository
from app.domain.value_objects.file_kind import FileKind
from app.application.dto.file_dto import FileResponse


class ListFilesForOwnerQuery:
    def __init__(self, repo: FileRepository):
        self.repo = repo

    def run(self, owner_id: str, kind: Optional[FileKind], limit: Optional[int]) -> List[FileResponse]:
        files = self.repo.list_files_for_owner(owner_id, kind, limit)
        return [FileResponse(f.id, f.owner_id, f.kind, f.path, f.filename, f.book_id, f.version) for f in files]
    
class ListFilesForBookQuery:
    def __init__(self, repo: FileRepository):
        self.repo = repo

    def run(self, book_id: str, kind: Optional[FileKind], limit: Optional[int]) -> List[FileResponse]:
        files = self.repo.list_files_for_book(book_id, kind, limit)
        return [FileResponse(f.id, f.owner_id, f.kind, f.path, f.filename, f.book_id, f.version) for f in files]