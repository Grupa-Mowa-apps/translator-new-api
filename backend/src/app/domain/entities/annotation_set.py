from dataclasses import dataclass
from backend.src.app.domain.value_objects.annotation_status import AnnotationStatus
from app.domain.errors import AnnotationSetErrors
from app.domain.constants import INITIAL_VERSION

@dataclass
class AnnotationSet:
    id: str
    book_id: str
    file_path: str

    status: AnnotationStatus = AnnotationStatus.EXTRACTED_FROM_MD_TO_XLSX
    version: int = INITIAL_VERSION

    def _update_version(self) -> None:
        self.version += 1

    def mark_translated(self) -> None:
        if self.status != AnnotationStatus.EXTRACTED_FROM_MD_TO_XLSX:
            raise ValueError(AnnotationSetErrors.MUST_BE_EXTRACTED_BEFORE_TRANSLATED)
        self.status = AnnotationStatus.TRANSLATED
        self._update_version()

    def mark_reviewed(self) -> None:
        if self.status != AnnotationStatus.TRANSLATED:
            raise ValueError(AnnotationSetErrors.MUST_BE_TRANSLATED_BEFORE_REVIEWED)
        self.status = AnnotationStatus.REVIEWED
        self._update_version()

    def mark_applied(self) -> None:
        if self.status != AnnotationStatus.REVIEWED:
            raise ValueError(AnnotationSetErrors.MUST_BE_REVIEWED_BEFORE_APPLIED)
        self.status = AnnotationStatus.APPLIED
        self._update_version()
    
    def __repr__(self):
        cls = self.__class__.__name__
        return (
            f"{cls}(id={self.id!r}, book_id={self.book_id!r}, status={self.status.name}, version={self.version}, "
            f"file_path={self.file_path!r})"
        )
    
    def __str__(self):
        return f"AnnotationSet [{self.status.name}] for book {self.book_id} (v{self.version})"