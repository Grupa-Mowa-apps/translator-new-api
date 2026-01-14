from app.domain.ports.book_repository import BookRepository
from app.domain.errors import BookErrors


class DeleteBookCommand:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def run(self, book_id: str) -> None:
        ok = self.repo.delete(book_id)
        if not ok:
            raise ValueError(BookErrors.BOOK_NOT_FOUND)