from app.application.dto.book_dto import BookResponse
from app.domain.ports.book_repository import BookRepository
from app.domain.errors import BookErrors


class GetBookQuery:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def execute(self, book_id: str) -> BookResponse:
        book = self.repo.get(book_id)
        if not book:
            raise ValueError(BookErrors.BOOK_NOT_FOUND)

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