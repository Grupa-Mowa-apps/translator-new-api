from app.domain.ports.book_repository import BookRepository
from app.application.dto.book_dto import BookResponse
from typing import List

class GetUserBooksQuery:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def execute(self, owner_id: str) -> List[BookResponse]:
        books = self.repo.list_books_for_owner(owner_id)
        return [BookResponse(
                    id=b.id,
                    owner_id=b.owner_id,
                    title=b.title, 
                    genre=b.genre,
                    quotation_marks=b.quotation_marks,
                    file_id=b.file_id,
                    status=b.status,
                    version=b.version
                ) for b in books]
