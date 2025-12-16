from app.domain.ports.book_repository import BookRepository
from app.application.dto.book_dto import BookResponse
from typing import List

class GetUserBooksCommand:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def run(self, owner_id: str) -> List[BookResponse]:
        books = self.repo.list_books_for_owner(owner_id)
        return [BookResponse(id=b.id, title=b.title, genre=b.genre) for b in books]