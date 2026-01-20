import logging
from app.domain.ports.excel_quotes_footnotes import ExcelQuotesFootnotesPort
from app.domain.ports.book_repository import BookRepository
from app.domain.errors import BookErrors, AnnotationSetErrors, FileErrors
from app.application.dto.parser_dto import ApplyParserTranslationsRequest, ApplyParserTranslationsResponse
from app.domain.ports.annotation_set_repository import AnnotationSetRepository
from app.domain.ports.file_repository import FileRepository
from app.domain.services.failed_annotation_application_service import FailedAnnotationApplicationService

logger = logging.getLogger(__name__)

class ApplyExcelTranslationsCommand:
    def __init__(
        self, 
        book_repo: BookRepository, 
        annotation_repo: AnnotationSetRepository,
        excel_port: ExcelQuotesFootnotesPort,
        file_repo: FileRepository,
        failed_service: FailedAnnotationApplicationService,
    ):
        self.book_repo = book_repo
        self.annotation_repo = annotation_repo
        self.excel_port = excel_port
        self.file_repo = file_repo
        self.failed_service = failed_service

    def execute(self, book_id: str, dto: ApplyParserTranslationsRequest) -> ApplyParserTranslationsResponse:
        logger.info(f"Applying translations for book: {book_id}")
        book = self.book_repo.get(book_id=book_id)
        if not book:
            raise ValueError(BookErrors.BOOK_NOT_FOUND)
        if not book.file_id:
            raise ValueError(BookErrors.FILE_NOT_FOUND)
        
        file = self.file_repo.get(file_id=book.file_id)
        if not file:
            raise ValueError(FileErrors.FILE_NOT_FOUND)

        annotation_set = self.annotation_repo.get(dto.annotation_set_id)
        if not annotation_set or annotation_set.book_id != book.id:
            raise ValueError(AnnotationSetErrors.ANNOTATION_SET_NOT_FOUND_FOR_BOOK)
        
        excel_path = annotation_set.file_path

        output_path, failed_list = self.excel_port.apply_translations_from_excel(
            excel_path=excel_path,
            md_input_path=file.path,
            md_output_path=file.path,
        )

        if failed_list:
            self.failed_service.save_batch(annotation_set.id, failed_list)
            logger.warning(f"Failed to apply {len(failed_list)} annotations for annotation_set: {annotation_set.id}")

        annotation_set.mark_applied()
        self.annotation_repo.update(annotation_set=annotation_set)

        book.mark_annotations_applied()
        self.book_repo.update(book=book)
        
        logger.info(f"Translations applied for book: {book_id}")

        return ApplyParserTranslationsResponse(
            annotation_set_id=annotation_set.id,
            status=annotation_set.status,
        )
