from pathlib import Path
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.infrastructure.db.dependencies import get_db
from app.infrastructure.db.repositories.file_repo_sqlalchemy import SqlAlchemyFileRepository
from app.application.dto.file_dto import FileResponse, UploadFileRequest
from app.application.commands.upload_file import UploadFileCommand
from app.application.queries.get_file import GetFileQuery
from app.domain.value_objects.file_kind import FileKind
from app.application.commands.delete_file import DeleteFileCommand
from app.application.queries.list_files import ListFilesForBookQuery, ListFilesForOwnerQuery
from app.infrastructure.files.file_storage_adapter import FileStorageAdapter

router = APIRouter(prefix="/files", tags=["files"])

def file_repo(db: Session) -> SqlAlchemyFileRepository:
    return SqlAlchemyFileRepository(db)

def file_storage() -> FileStorageAdapter:
    return FileStorageAdapter(base_dir=Path("storage"))

@router.post("", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    owner_id: str = Form(...),
    kind: FileKind = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        content = await file.read()
        cmd = UploadFileCommand(repo=file_repo(db=db), storage=file_storage())
        return cmd.execute(
            owner_id=owner_id,
            filename=file.filename or "file",
            content=content,
            content_type=file.content_type,
            kind=kind,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{file_id}", response_model=FileResponse, status_code=status.HTTP_200_OK)
def get_file(file_id: str, db: Session = Depends(get_db)):
    try:
        return GetFileQuery(file_repo(db)).execute(file_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@router.get("/by-owner/{owner_id}", response_model=List[FileResponse], status_code=status.HTTP_200_OK)
def list_files_for_owner(
    owner_id: str, 
    kind: Optional[FileKind] = Query(None), 
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return ListFilesForOwnerQuery(file_repo(db)).execute(owner_id, kind, limit)

@router.get("/by-book/{book_id}", response_model=List[FileResponse], status_code=status.HTTP_200_OK)
def list_files_for_book(
    book_id: str,
    kind: Optional[FileKind] = Query(None), 
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return ListFilesForBookQuery(file_repo(db)).execute(book_id, kind, limit)

@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(file_id: str, db: Session = Depends(get_db)):
    try:
        DeleteFileCommand(file_repo(db), file_storage()).execute(file_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))