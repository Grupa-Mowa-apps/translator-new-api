from typing import Optional
from pydantic import BaseModel
from app.domain.value_objects.file_kind import FileKind

class UploadFileRequest(BaseModel):
    owner_id: str
    kind: FileKind
    filename: str
    book_id: str

class UpdateFileRequest(BaseModel):
    owner_id: Optional[str]
    kind: Optional[FileKind]
    filename: Optional[str]
    book_id: Optional[str]

class FileResponse(BaseModel):
    id: str
    owner_id: str
    kind: FileKind
    path: str
    filename: str
    book_id: str
    version: int