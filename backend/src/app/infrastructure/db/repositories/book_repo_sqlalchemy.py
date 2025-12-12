from sqlalchemy.orm import Session
from app.domain.ports.book_repository import BookRepository
from app.domain.entities.book import Book
from app.domain.entities.chapter import Chapter
from app.infrastructure.db.models import BookDB, ChapterDB
from app.domain.errors import BookErrors
from typing import Optional, Iterable

def _row_to_domain_book(book: BookDB) -> Book:
    return Book(id=book.id, owner_id=book.owner_id,
                title=book.title, genre=book.genre, quotation_marks=book.quotation_marks,
                file_path=book.file_path,
                chapters=[_row_to_domain_chapter(ch) for ch in book.chapters],
                status=book.status, version=book.version
                )

def _row_to_domain_chapter(chapter: ChapterDB) -> Chapter:
    return Chapter(id=chapter.id, book_id=chapter.book_id, parent_id=chapter.parent_id,
                   chapter_number=chapter.chapter_number, title=chapter.title,
                   content=chapter.content
                   )

class SqlAlchemyBookRepository(BookRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, book: Book) -> None:
        self.session.add(BookDB(
            id=book.id, owner_id=book.owner_id,
            title=book.title, genre=book.genre, quotation_marks=book.quotation_marks,
            file_path=book.file_path,
            status=book.status, version=book.version
        ))
        self.session.commit()

    def get(self, book_id: str) -> Optional[Book]:
        # [CODE REVIEW] [BLOCKER] Analogicznie jak w innych repozytoriach - get() powinno zwracać None,
        # nie rzucać wyjątku. Warstwa infrastructure nie powinna decydować o logice biznesowej.
        book_row = self.session.get(BookDB, book_id)
        if not book_row:
            raise ValueError(BookErrors.BOOK_NOT_FOUND)
        return _row_to_domain_book(book_row)
    
    def get_by_title(self, title: str) -> Optional[Book]:
        book_row = self.session.query(BookDB).filter(BookDB.title == title).first()
        if not book_row:
            raise ValueError(BookErrors.BOOK_NOT_FOUND)
        return _row_to_domain_book(book_row)
    
    def update(self, book: Book) -> None:
        book_row = self.session.get(BookDB, book.id)
        if not book_row:
            raise ValueError(BookErrors.BOOK_NOT_FOUND)
        book_row.title = book.title
        book_row.genre = book.genre
        book_row.quotation_marks = book.quotation_marks
        book_row.file_path = book.file_path
        book_row.status = book.status
        book_row.version = book.version
        self.session.commit()

    def delete(self, book_id: str) -> None:
        book_row = self.session.get(BookDB, book_id)
        if not book_row:
            raise ValueError(BookErrors.BOOK_NOT_FOUND)
        self.session.delete(book_row)
        self.session.commit()

    def list_books_for_owner(self, owner_id: str) -> Iterable[Book]:
        book_rows = self.session.query(BookDB).filter(BookDB.owner_id == owner_id).all()
        return [_row_to_domain_book(book_row) for book_row in book_rows]