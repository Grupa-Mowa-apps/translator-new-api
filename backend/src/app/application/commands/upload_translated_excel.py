import uuid
from app.application.dto.parser_dto import UploadTranslatedExcelRequest, UploadTranslatedExcelResponse
from app.domain.constants import EXCEl_FILE_EXTENSION
from app.domain.entities.annotation_set import AnnotationSet
from app.domain.errors import BookErrors, AnnotationSetErrors
from app.domain.ports.annotation_set_repository import AnnotationSetRepository
from app.domain.ports.book_repository import BookRepository
from app.domain.ports.file_storage import FileStorage
from app.domain.value_objects.annotation_status import AnnotationStatus


class UploadTranslatedExcelCommand:
    def __init__(
        self,
        book_repo: BookRepository,
        annotation_repo: AnnotationSetRepository,
        file_storage: FileStorage,
    ):
        self.book_repo = book_repo
        self.annotation_repo = annotation_repo
        self.file_storage = file_storage

    def run(self, dto: UploadTranslatedExcelRequest) -> UploadTranslatedExcelResponse:
        book = self.book_repo.get(book_id=dto.book_id)
        if book is None:
            raise ValueError(BookErrors.BOOK_NOT_FOUND)
        
        name = dto.filename.strip()
        if not name.endswith(EXCEl_FILE_EXTENSION):
            raise ValueError(AnnotationSetErrors.INVALID_EXCEL_FILE_TYPE)
        
        storage_path = self.file_storage.save(
            owner_id=book.owner_id,
            filename=dto.filename,
            content=dto.content,
            content_type=dto.content_type,
        )

        annotation_set = AnnotationSet(
            id=uuid.uuid4().hex,
            book_id=book.id,
            file_path=storage_path,
            status=AnnotationStatus.TRANSLATED,
        )
        self.annotation_repo.add(annotation_set=annotation_set)

        return UploadTranslatedExcelResponse(
            annotation_set_id=annotation_set.id,
            book_id=annotation_set.book_id,
            excel_path=annotation_set.file_path,
            status=annotation_set.status,
        )