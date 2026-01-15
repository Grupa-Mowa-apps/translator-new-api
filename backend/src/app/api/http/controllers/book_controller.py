import os
from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.application.commands.process_book import ProcessBookCommand
from app.application.queries.get_book_with_chapters import GetBookWithChaptersQuery
from app.infrastructure.book.book_mapper_adapter import BookMapperAdapter
from app.infrastructure.db.dependencies import get_db
from app.infrastructure.db.repositories.book_repo_sqlalchemy import SqlAlchemyBookRepository
from app.infrastructure.db.repositories.chapter_repo_sqlalchemy import SqlAlchemyChapterRepository
from app.infrastructure.db.repositories.file_repo_sqlalchemy import SqlAlchemyFileRepository

from app.application.dto.book_dto import BookWithChaptersResponse, CreateBookRequest, BookResponse, ProcessBookRequest
from app.application.dto.chapter_dto import ChapterResponse
from app.application.commands.create_book_from_file import CreateBookFromFileCommand
from app.application.queries.get_book import GetBookQuery
from app.application.queries.list_books import ListBooksForOwnerQuery
from app.infrastructure.files.file_storage_adapter import FileStorageAdapter
from app.infrastructure.parsing.markdown_analyzer_adapter import MarkdownAnalyzerAdapter

router = APIRouter(prefix="/books", tags=["books"])


def book_repo(db: Session) -> SqlAlchemyBookRepository:
    return SqlAlchemyBookRepository(session=db)

def file_repo(db: Session) -> SqlAlchemyFileRepository:
    return SqlAlchemyFileRepository(session=db)

def chapter_repo(db: Session) -> SqlAlchemyChapterRepository:
    return SqlAlchemyChapterRepository(session=db)

def file_storage() -> FileStorageAdapter:
    return FileStorageAdapter()

def book_mapper() -> BookMapperAdapter:
    base_dir = Path(os.environ.get("FILE_STORAGE_DIR", "/app/backend/storage"))

    md_analyzer_factory = lambda rel_path: MarkdownAnalyzerAdapter(
        file_path=str((base_dir / rel_path).resolve())
    )
    return BookMapperAdapter(md_analyzer_factory=md_analyzer_factory)
    

@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(dto: CreateBookRequest, db: Session = Depends(get_db)):
    try:
        cmd = CreateBookFromFileCommand(
            book_repo=book_repo(db),
            file_repo=file_repo(db),
        )
        return cmd.execute(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
def get_book(book_id: str, db: Session = Depends(get_db)):
    try:
        return GetBookQuery(book_repo(db)).execute(book_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("", response_model=list[BookResponse], status_code=status.HTTP_200_OK)
def list_books(owner_id: str, db: Session = Depends(get_db)):
    try:
        return ListBooksForOwnerQuery(book_repo(db)).execute(owner_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post("/{book_id}/map", response_model=BookResponse, status_code=status.HTTP_200_OK)
def mapp_book(book_id: str, db: Session = Depends(get_db)):
    try:
        cmd = ProcessBookCommand(
            book_repo=book_repo(db),
            file_repo=file_repo(db),
            chapter_repo=chapter_repo(db),
            file_storage=file_storage(),
            book_mapper=book_mapper(),
        )
        return cmd.execute(dto=ProcessBookRequest(book_id=book_id))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/{book_id}/chapters", response_model=list[ChapterResponse], status_code=status.HTTP_200_OK)
def list_chapters(book_id: str, db: Session = Depends(get_db)):
    rows = list(chapter_repo(db).list_for_book(book_id))
    return [
        ChapterResponse(
            id=chapter.id,
            book_id=chapter.book_id,
            chapter_number=chapter.chapter_number,
            title=chapter.title,
            parent_id=chapter.parent_id,
            content=chapter.content.text,
        )
        for chapter in rows
    ]

@router.get("/{book_id}/full", response_model=BookWithChaptersResponse)
def get_book_full(book_id: str, db: Session = Depends(get_db)):
    try:
        query = GetBookWithChaptersQuery(
            book_repo=book_repo(db),
            chapter_repo=chapter_repo(db),
        )
        book = query.execute(book_id)

        return BookWithChaptersResponse(
            id=book.id,
            owner_id=book.owner_id,
            title=book.title,
            genre=book.genre,
            quotation_marks=book.quotation_marks,
            file_id=book.file_id,
            status=book.status.value,
            version=book.version,
            chapters=[
                ChapterResponse(
                    id=ch.id,
                    book_id=ch.book_id,
                    chapter_number=ch.chapter_number,
                    title=ch.title,
                    parent_id=ch.parent_id,
                    content=ch.content.text if ch.content else None,
                )
                for ch in book.chapters
            ],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))