""" This module implements a command for mapping file content into Book entity """

import uuid
import logging
from app.application.dto.book_dto import BookResponse, ProcessBookRequest
from app.domain.entities.chapter import Chapter
from app.domain.errors import BookErrors, FileErrors
from app.domain.ports.book_mapper_port import BookMapperPort
from app.domain.ports.book_repository import BookRepository
from app.domain.ports.chapter_repository import ChapterRepository
from app.domain.ports.file_repository import FileRepository
from app.domain.ports.file_storage import FileStorage
from app.domain.value_objects.chapter_content import ChapterContent

logger = logging.getLogger(__name__)


class ProcessBookCommand:
    def __init__(
        self,
        book_repo: BookRepository,
        file_repo: FileRepository,
        chapter_repo: ChapterRepository,
        file_storage: FileStorage,
        book_mapper: BookMapperPort,
    ):
        self.book_repo = book_repo
        self.file_repo = file_repo
        self.chapter_repo = chapter_repo
        self.file_storage = file_storage
        self.book_mapper = book_mapper

    def run(self, dto: ProcessBookRequest) -> BookResponse:
        logger.info(f"Processing book: {dto.book_id}")
        book = self.book_repo.get(book_id=dto.book_id)

        if book is None:
            raise ValueError(BookErrors.BOOK_NOT_FOUND)
        if book.file_id is None:
            raise ValueError(BookErrors.FILE_NOT_FOUND)
        
        file = self.file_repo.get(file_id=book.file_id)
        if file is None:
            raise ValueError(FileErrors.FILE_NOT_FOUND)
        
        try:
            raw_chapters = self.book_mapper.map_chapters(
                file_path=file.path,
            )

            chapters = []
            number_to_id = {}

            for raw_chapter in raw_chapters:
                chapter_id = uuid.uuid4().hex
                number = int(raw_chapter["number"])
                number_to_id[number] = chapter_id

                chapters.append(
                    Chapter(
                        id=chapter_id,
                        book_id=book.id,
                        chapter_number=number,
                        title=str(raw_chapter.get("title", "")).strip(),
                        parent_id=None,
                        content=ChapterContent(text=str(raw_chapter.get("text", "") or ""))
                    )
                )

            for chapter, raw_chapter in zip(chapters, raw_chapters):
                parent_number = raw_chapter.get("parent_number")
                if parent_number is not None:
                    chapter.set_parent(number_to_id[int(parent_number)])

            self.chapter_repo.delete_for_book(book_id=book.id)
            self.chapter_repo.add_many(chapters=chapters)

            book.mark_mapped()
            self.book_repo.update(book=book)
            
            self.book_repo.session.commit()
            logger.info(f"Book processed successfully: {book.id}")

        except Exception as e:
            book.mark_failed()
            self.book_repo.update(book=book)
            self.book_repo.session.commit()
            logger.error(f"Book processing failed: {book.id} - {e}")
            raise ValueError(f"{BookErrors.BOOK_MAPPING_FAILED}: {e}") from e 
        
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