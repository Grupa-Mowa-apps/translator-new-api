import logging
from app.domain.ports.book_repository import BookRepository

logger = logging.getLogger(__name__)

class DeleteBookCommand:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def execute(self, book_id: str, owner_id: str) -> None:
        logger.info(f"Deleting book: {book_id} for owner: {owner_id}")
        
        book = self.repo.get(book_id)
        if not book:
            logger.warning(f"Book not found: {book_id}")
            raise ValueError("Book not found")
        
        if book.owner_id != owner_id:
            logger.warning(f"Book {book_id} does not belong to owner {owner_id}")
            raise ValueError("Book does not belong to this user")
        
        self.repo.delete(book_id)
        logger.info(f"Book deleted successfully: {book_id}")
