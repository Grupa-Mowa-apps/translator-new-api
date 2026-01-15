import logging
from app.domain.ports.book_repository import BookRepository
from app.domain.errors import BookErrors

logger = logging.getLogger(__name__)

class DeleteBookCommand:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def execute(self, book_id: str) -> None:
        logger.info(f"Deleting book: {book_id}")
        ok = self.repo.delete(book_id)
        if not ok:
            raise ValueError(BookErrors.BOOK_NOT_FOUND)
        logger.info(f"Book deleted: {book_id}")