import logging
from app.application.dto.book_dto import UpdateBookRequest, BookResponse
from app.domain.ports.book_repository import BookRepository
from app.domain.errors import BookErrors

logger = logging.getLogger(__name__)

class UpdateBookCommand:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def execute(self, book_id: str, dto: UpdateBookRequest) -> BookResponse:
        logger.info(f"Updating book: {book_id}")
        book = self.repo.get(book_id)
        if not book:
            raise ValueError(BookErrors.BOOK_NOT_FOUND)

        if dto.title is not None:
            book.title = dto.title
        if dto.genre is not None:
            book.genre = dto.genre
        if dto.quotation_marks is not None:
            book.quotation_marks = dto.quotation_marks
        if dto.file_id is not None:
            book.file_id = dto.file_id
        if dto.status is not None:
            book.status = dto.status
        if dto.version is not None:
            book.version = dto.version

        ok = self.repo.update(book)
        if not ok:
            raise ValueError(BookErrors.BOOK_NOT_FOUND)
        
        logger.info(f"Book updated: {book_id}")

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
