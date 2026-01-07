from app.domain.entities.book import Book
from app.domain.ports.book_repository import BookRepository
from app.domain.ports.chapter_repository import ChapterRepository
from app.domain.errors import BookErrors


class GetBookWithChaptersQuery:
    def __init__(
        self,
        book_repo: BookRepository,
        chapter_repo: ChapterRepository,
    ):
        self.book_repo = book_repo
        self.chapter_repo = chapter_repo

    def run(self, book_id: str) -> Book:
        book = self.book_repo.get(book_id)
        if not book:
            raise ValueError(BookErrors.BOOK_NOT_FOUND)

        chapters = list(self.chapter_repo.list_for_book(book_id))
        book.chapters = chapters

        return book