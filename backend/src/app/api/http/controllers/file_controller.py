from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
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

router = APIRouter(prefix="/files", tags=["files"])

def file_repo(db: Session):
    return SqlAlchemyFileRepository(db)

@router.post("", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(dto: UploadFileRequest, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # [CODE REVIEW] [SUGGESTION] Zmienna 'content' jest nieużywana - czy upload faktycznie zapisuje plik?
    # Wygląda na to, że plik jest tylko odczytywany ale nigdzie nie zapisywany.
    content = await file.read()
    return UploadFileCommand(file_repo(db)).run(dto)

@router.get("/{file_id}", response_model=FileResponse, status_code=status.HTTP_200_OK)
def get_file(file_id: str, db: Session = Depends(get_db)):
    try:
        return GetFileQuery(file_repo(db)).run(file_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
# [CODE REVIEW] [BLOCKER] Błąd: ścieżka ma {book_id} ale funkcja przyjmuje owner_id.
# Powinno być: "/by-owner/{owner_id}" lub zmiana parametru na book_id
@router.get("/by-owner/{book_id}", response_model=List[FileResponse], status_code=status.HTTP_200_OK)
def list_files_for_owner(
    owner_id: str, 
    kind: Optional[FileKind] = Query(None), 
    limit: int = Query(None), 
    db: Session = Depends(get_db)
):
    return ListFilesForOwnerQuery(file_repo(db)).run(owner_id, kind, limit)

@router.get("/by-book/{book_id}", response_model=List[FileResponse], status_code=status.HTTP_200_OK)
def list_files_for_book(
    book_id: str,
    kind: Optional[FileKind] = Query(None), 
    limit: int = Query(None), 
    db: Session = Depends(get_db)
):
    return ListFilesForBookQuery(file_repo(db)).run(book_id, kind, limit)

@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(file_id: str, db: Session = Depends(get_db)):
    try:
        DeleteFileCommand(file_repo(db)).run(file_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))