from typing import List, Optional
from sqlalchemy.orm import Session
from app.infrastructure.db.models import FileDB
from app.domain.entities.file import File
from app.domain.value_objects.file_kind import FileKind
from app.domain.ports.file_repository import FileRepository

def _row_to_domain_file(file_row: FileDB) -> File:
    return File(
        id=file_row.id, 
        owner_id=file_row.owner_id,
        kind=FileKind(file_row.kind), 
        path=file_row.path, 
        filename=file_row.filename,
        book_id=file_row.book_id, 
        version=file_row.version,
    )

def _domain_to_row_file(file: File) -> FileDB:
    return FileDB(
        id=file.id, 
        owner_id=file.owner_id,
        kind=file.kind.value, 
        path=file.path, 
        filename=file.filename,
        book_id=file.book_id, 
        version=file.version,
    )

class SqlAlchemyFileRepository(FileRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    def add(self, file: File) -> None:
        file_row = _domain_to_row_file(file)
        self.session.add(file_row)

    def get(self, file_id: str) -> Optional[File]:
        file_row = self.session.get(FileDB, file_id)
        if not file_row:
            return None
        return _row_to_domain_file(file_row)
    
    def update(self, file: File) -> None:
        file_row = self.session.get(FileDB, file.id)
        if not file_row:
            return None
        file_row.owner_id = file.owner_id
        file_row.kind = file.kind.value
        file_row.path = file.path
        file_row.filename = file.filename
        file_row.book_id = file.book_id
        file_row.version = file.version

    def delete(self, file_id: str) -> None:
        file_row = self.session.get(FileDB, file_id)
        if not file_row:
            return None
        self.session.delete(file_row)

    def list_files_for_owner(self, owner_id: str, kind: Optional[FileKind], limit: Optional[int]) -> List[File]:
        file_rows = self.session.query(FileDB).filter(FileDB.owner_id == owner_id)
        if kind:
            file_rows = file_rows.filter(FileDB.kind == kind.value)
        if limit:
            file_rows = file_rows.order_by(FileDB.filename.asc()).limit(limit)
        return [_row_to_domain_file(file_row) for file_row in file_rows.all()]

    def list_files_for_book(self, book_id: str, kind: Optional[FileKind], limit: Optional[int]) -> List[File]:
        file_rows = self.session.query(FileDB).filter(FileDB.book_id == book_id)
        if kind:
            file_rows = file_rows.filter(FileDB.kind == kind.value)
        if limit:
            file_rows = file_rows.order_by(FileDB.filename.asc()).limit(limit)
        return [_row_to_domain_file(file_row) for file_row in file_rows.all()]