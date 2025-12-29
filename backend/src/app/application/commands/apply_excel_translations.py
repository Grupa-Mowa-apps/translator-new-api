from app.domain.ports.excel_quotes_footnotes import ExcelQuotesFootnotesPort
from app.domain.ports.book_repository import BookRepository
from app.domain.errors import BookErrors
from app.application.dto.parser_dto import ApplyParserTranslationsRequest, ApplyParserTranslationsResponse

class ApplyExcelTranslationsCommand:
    def __init__(self, book_repo: BookRepository, excel_port: ExcelQuotesFootnotesPort):
        self.book_repo = book_repo
        self.excel_port = excel_port

    def run(self, book_id: str, dto: ApplyParserTranslationsRequest) -> ApplyParserTranslationsResponse:
        book = self.book_repo.get(book_id)
        if not book:
            raise ValueError(BookErrors.BOOK_NOT_FOUND)

        if not book.file_path:
            raise ValueError(BookErrors.BOOK_FILE_PATH_NOT_SET)

        output_md_path = self.excel_port.apply_translations_from_excel(
            excel_path=dto.excel_path,
            md_input_path=book.file_path,
            output_md_filename=dto.output_md_filename,
        )

        return ApplyParserTranslationsResponse(output_md_path=output_md_path)
