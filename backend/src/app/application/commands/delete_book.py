import logging
from app.domain.ports.book_repository import BookRepository
from app.domain.errors import BookErrors

logger = logging.getLogger(__name__)

class DeleteBookCommand:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def run(self, book_id: str) -> None:
        logger.info(f"Deleting book: {book_id}")
        ok = self.repo.delete(book_id)
        if not ok:
            raise ValueError(BookErrors.BOOK_NOT_FOUND)
        self.repo.session.commit()
        logger.info(f"Book deleted: {book_id}")