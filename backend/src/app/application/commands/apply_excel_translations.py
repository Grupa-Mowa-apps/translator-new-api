from app.domain.ports.excel_quotes_footnotes import ExcelQuotesFootnotesPort
from app.domain.ports.book_repository import BookRepository
from app.domain.errors import BookErrors, AnnotationSetErrors
from app.application.dto.parser_dto import ApplyParserTranslationsRequest, ApplyParserTranslationsResponse
from app.domain.ports.annotation_set_repository import AnnotationSetRepository

class ApplyExcelTranslationsCommand:
    def __init__(
        self, 
        book_repo: BookRepository, 
        annotation_repo: AnnotationSetRepository,
        excel_port: ExcelQuotesFootnotesPort,
    ):
        self.book_repo = book_repo
        self.annotation_repo = annotation_repo
        self.excel_port = excel_port

    def run(self, book_id: str, dto: ApplyParserTranslationsRequest) -> ApplyParserTranslationsResponse:
        book = self.book_repo.get(book_id=book_id)
        if not book:
            raise ValueError(BookErrors.BOOK_NOT_FOUND)
        if not book.file_path:
            raise ValueError(BookErrors.BOOK_FILE_PATH_NOT_SET)

        annotation_set = self.annotation_repo.get(dto.annotation_set_id)
        if not annotation_set or annotation_set.book_id != book.id:
            raise ValueError(AnnotationSetErrors.ANNOTATION_SET_NOT_FOUND_FOR_BOOK)

        output_md_path = self.excel_port.apply_translations_from_excel(
            excel_path=dto.excel_path,
            md_input_path=book.file_path,
            md_output_path=dto.output_md_filename,
        )

        annotation_set.mark_applied()
        book.mark_annotations_applied()

        return ApplyParserTranslationsResponse(output_md_path=output_md_path)
