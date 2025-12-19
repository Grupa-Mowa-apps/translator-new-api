import uuid
from app.domain.ports.excel_quotes_footnotes import ExcelQuotesFootnotesPort
from app.domain.ports.book_repository import BookRepository
from app.domain.errors import BookErrors
from app.application.dto.parser_dto import ExportParserRequest, ExportParserResponse
from app.domain.ports.annotation_set_repository import AnnotationSetRepository
from app.domain.entities.annotation_set import AnnotationSet

class ExportQuotesFootnotesCommand:
    def __init__(
        self, 
        book_repo: BookRepository,
        annotation_repo: AnnotationSetRepository,
        excel_port: ExcelQuotesFootnotesPort,
    ):
        self.book_repo = book_repo
        self.annotation_repo = annotation_repo
        self.excel_port = excel_port

    def run(self, book_id: str, dto: ExportParserRequest) -> ExportParserResponse:
        book = self.book_repo.get(book_id=book_id)
        if not book:
            raise ValueError(BookErrors.BOOK_NOT_FOUND)    
        if not book.file_path:
            raise ValueError(BookErrors.BOOK_FILE_PATH_NOT_SET)

        excel_path, stats = self.excel_port.export_from_markdown(
            md_path=book.file_path,
            quote_type=dto.quote_type,
            excel_path=dto.excel_filename,
        )

        annotation_set = AnnotationSet(
            id=str(uuid.uuid64()),
            book_id=book_id,
            file_path=excel_path,
        )
        self.annotation_repo.add(annotation_set=annotation_set)

        book.mark_parsed()
        self.book_repo.update(book=book)

        return ExportParserResponse(
            excel_path=excel_path,
            footnotes_count=stats["footnotes"],
            quotes_count=stats["quotes"],
            blockquotes_count=stats["blockquotes"],
        )