from typing import Optional
from pydantic import BaseModel
from app.domain.value_objects.file_kind import FileKind

class UploadFileRequest(BaseModel):
    owner_id: str
    kind: FileKind
    filename: str
    book_id: Optional[str] = None

class UpdateFileRequest(BaseModel):
    owner_id: Optional[str] = None
    kind: Optional[FileKind] = None
    filename: Optional[str] = None
    book_id: Optional[str] = None

class FileResponse(BaseModel):
    id: str
    owner_id: str
    kind: FileKind
    path: str
    filename: str
    book_id: Optional[str] = None
    version: int