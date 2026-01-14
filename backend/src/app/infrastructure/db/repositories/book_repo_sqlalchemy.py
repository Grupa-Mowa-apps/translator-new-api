from sqlalchemy.orm import Session
from app.domain.ports.book_repository import BookRepository
from app.domain.entities.book import Book
from app.domain.entities.chapter import Chapter
from app.infrastructure.db.models import BookDB, ChapterDB
from typing import Optional, Iterable

from app.domain.value_objects.quotation_marks import QuoteType
from app.domain.value_objects.book_status import BookStatus

def _row_to_domain_book(row: BookDB) -> Book:
    return Book(
        id=row.id, 
        owner_id=row.owner_id,
        title=row.title, 
        genre=row.genre, 
        quotation_marks=QuoteType(row.quotation_marks),
        file_id=row.file_id,
        chapters=[_row_to_domain_chapter(ch) for ch in row.chapters],
        status=BookStatus(row.status), 
        version=row.version,
    )

def _row_to_domain_chapter(chapter: ChapterDB) -> Chapter:
    return Chapter(
        id=chapter.id, 
        book_id=chapter.book_id, 
        parent_id=chapter.parent_id,
        chapter_number=chapter.chapter_number, 
        title=chapter.title,
        content=chapter.content,
    )

class SqlAlchemyBookRepository(BookRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, book: Book) -> None:
        self.session.add(
            BookDB(
                id=book.id, 
                owner_id=book.owner_id,
                title=book.title, 
                genre=book.genre, 
                quotation_marks=book.quotation_marks.value,
                file_id=book.file_id,
                status=book.status.value, 
                version=book.version,
        ))

    def get(self, book_id: str) -> Optional[Book]:
        book_row = self.session.get(BookDB, book_id)
        if book_row is None:
            return None
        return _row_to_domain_book(book_row)
    
    def get_by_title(self, title: str) -> Optional[Book]:
        book_row = self.session.query(BookDB).filter(BookDB.title == title).first()
        if book_row is None:
            return None
        return _row_to_domain_book(book_row)
    
    def update(self, book: Book) -> bool:
        book_row = self.session.get(BookDB, book.id)
        if book_row is None:
            return False
        book_row.title = book.title
        book_row.genre = book.genre
        book_row.quotation_marks = book.quotation_marks
        book_row.file_id = book.file_id
        book_row.status = book.status
        book_row.version = book.version
        return True

    def delete(self, book_id: str) -> bool:
        book_row = self.session.get(BookDB, book_id)
        if book_row is None:
            return False
        self.session.delete(book_row)
        return True

    def list_books_for_owner(self, owner_id: str) -> Iterable[Book]:
        book_rows = self.session.query(BookDB).filter(BookDB.owner_id == owner_id).all()
        return [_row_to_domain_book(book_row) for book_row in book_rows]