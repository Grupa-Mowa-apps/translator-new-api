from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.infrastructure.db.dependencies import get_db
from app.infrastructure.db.repositories.book_repo_sqlalchemy import SqlAlchemyBookRepository
from app.infrastructure.db.repositories.file_repo_sqlalchemy import SqlAlchemyFileRepository

from app.application.dto.book_dto import CreateBookRequest, BookResponse
from app.application.commands.create_book_from_file import CreateBookFromFileCommand
from app.application.queries.get_book import GetBookQuery
from app.application.queries.list_books import ListBooksForOwnerQuery


router = APIRouter(prefix="/books", tags=["books"])


def book_repo(db: Session) -> SqlAlchemyBookRepository:
    return SqlAlchemyBookRepository(db)


def file_repo(db: Session) -> SqlAlchemyFileRepository:
    return SqlAlchemyFileRepository(db)


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(dto: CreateBookRequest, db: Session = Depends(get_db)):
    try:
        cmd = CreateBookFromFileCommand(
            book_repo=book_repo(db),
            file_repo=file_repo(db),
        )
        return cmd.run(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
def get_book(book_id: str, db: Session = Depends(get_db)):
    try:
        return GetBookQuery(book_repo(db)).run(book_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("", response_model=list[BookResponse], status_code=status.HTTP_200_OK)
def list_books(owner_id: str, db: Session = Depends(get_db)):
    try:
        return ListBooksForOwnerQuery(book_repo(db)).run(owner_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
