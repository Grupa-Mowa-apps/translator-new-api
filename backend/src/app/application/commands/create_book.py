import uuid
import logging

from app.application.dto.book_dto import CreateBookRequest, BookResponse
from app.domain.entities.book import Book
from app.domain.ports.book_repository import BookRepository
from app.domain.errors import BookErrors

logger = logging.getLogger(__name__)

class CreateBookCommand:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def execute(self, dto: CreateBookRequest) -> BookResponse:
        existing = self.repo.get_by_title(dto.title)
        if existing and existing.owner_id == dto.owner_id:
            raise ValueError(BookErrors.TITLE_ALREADY_EXISTS)

        book = Book(
            id=uuid.uuid4().hex,
            owner_id=dto.owner_id,
            title=dto.title,
            genre=dto.genre,
            quotation_marks=dto.quotation_marks,
            file_id=dto.file_id,
            chapters=[],
        )
        self.repo.add(book)
        logger.info(f"Book created: {book.id} - {book.title}")

        return BookResponse(
            id=book.id,
            owner_id=book.owner_id,
            title=book.title,
            genre=book.genre,
            quotation_marks=book.quotation_marks,
            file_id=book.file_id,
            status=book.status,
            version=book.version,
        )
