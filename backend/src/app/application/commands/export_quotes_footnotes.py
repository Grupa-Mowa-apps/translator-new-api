import uuid
import logging
from app.domain.ports.excel_quotes_footnotes import ExcelQuotesFootnotesPort
from app.domain.ports.book_repository import BookRepository
from app.domain.errors import BookErrors, FileErrors
from app.application.dto.parser_dto import ExportParserRequest, ExportParserResponse
from app.domain.ports.annotation_set_repository import AnnotationSetRepository
from app.domain.entities.annotation_set import AnnotationSet
from app.domain.ports.file_repository import FileRepository

logger = logging.getLogger(__name__)

class ExportQuotesFootnotesCommand:
    def __init__(
        self, 
        book_repo: BookRepository,
        annotation_repo: AnnotationSetRepository,
        excel_port: ExcelQuotesFootnotesPort,
        file_repo: FileRepository,
    ):
        self.book_repo = book_repo
        self.annotation_repo = annotation_repo
        self.excel_port = excel_port
        self.file_repo = file_repo

    def execute(self, book_id: str, dto: ExportParserRequest) -> ExportParserResponse:
        logger.info(f"Exporting quotes/footnotes for book: {book_id}")
        book = self.book_repo.get(book_id=book_id)
        if not book:
            raise ValueError(BookErrors.BOOK_NOT_FOUND)    
        if not book.file_id:
            raise ValueError(BookErrors.FILE_NOT_FOUND)
        
        file = self.file_repo.get(file_id=book.file_id)
        if not file:
            raise ValueError(FileErrors.FILE_NOT_FOUND)

        excel_path, stats = self.excel_port.export_from_markdown(
            md_path=file.path,
            quote_type=dto.quote_type,
            excel_path=dto.excel_filename,
        )

        annotation_set = AnnotationSet(
            id=uuid.uuid4().hex,
            book_id=book_id,
            file_path=excel_path,
        )
        self.annotation_repo.add(annotation_set=annotation_set)

        book.mark_parsed()
        self.book_repo.update(book=book)
        
        logger.info(f"Exported quotes/footnotes for book: {book_id} to {excel_path}")

        return ExportParserResponse(
            annotation_set_id=annotation_set.id,
            excel_path=excel_path,
            footnotes_count=stats["footnotes"],
            quotes_count=stats["quotes"],
            blockquotes_count=stats["blockquotes"],
        )