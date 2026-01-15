import uuid
import logging
from app.domain.ports.book_repository import BookRepository
from app.domain.ports.file_repository import FileRepository
from app.application.dto.book_dto import BookResponse, CreateBookRequest
from app.domain.errors import BookErrors, FileErrors
from app.domain.entities.book import Book

logger = logging.getLogger(__name__)

class CreateBookFromFileCommand:
    def __init__(self, book_repo: BookRepository, file_repo: FileRepository):
        self.book_repo = book_repo
        self.file_repo = file_repo

    def execute(self, dto: CreateBookRequest) -> BookResponse:
        logger.info(f"Creating book from file: {dto.file_id}")
        file = self.file_repo.get(dto.file_id)
        if not file:
            raise ValueError(FileErrors.FILE_NOT_FOUND)
        
        existing = self.book_repo.get_by_title(dto.title)
        if existing and existing.owner_id == dto.owner_id:
            raise ValueError(BookErrors.TITLE_ALREADY_EXISTS)

        book = Book(
            id=uuid.uuid4().hex,
            owner_id=dto.owner_id,
            title=dto.title,
            genre=dto.genre,
            quotation_marks=dto.quotation_marks,
            file_id=dto.file_id,
            chapters=[],
        )
        self.book_repo.add(book=book)

        file.attach_to_book(book_id=book.id)
        self.file_repo.update(file=file)
        
        logger.info(f"Book created from file: {book.id} - {book.title}")

        return BookResponse(
            id=book.id,
            owner_id=book.owner_id,
            title=book.title,
            genre=book.genre,
            quotation_marks=book.quotation_marks,
            file_id=book.file_id,
            status=book.status.value,
            version=book.version,
        )