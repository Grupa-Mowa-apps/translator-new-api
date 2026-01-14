from app.application.dto.book_dto import BookResponse
from app.domain.ports.book_repository import BookRepository
from app.domain.errors import BookErrors


class GetBookByTitleQuery:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def run(self, title: str) -> BookResponse:
        book = self.repo.get_by_title(title)
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