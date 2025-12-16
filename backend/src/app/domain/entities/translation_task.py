from dataclasses import dataclass
from typing import Optional
from app.domain.value_objects.translation_status import TranslationStatus
from app.domain.errors import TranslationTaskErrors
from app.domain.constants import INITIAL_PROGRESS, INITIAL_TRANSLATED_CHAPTERS

@dataclass
class TranslationTask:
    id: str
    book_id: str

    total_chapters: Optional[int] = None
    message: Optional[str] = None

    status: TranslationStatus = TranslationStatus.QUEUED
    progress: int = INITIAL_PROGRESS
    translated_chapters: int = INITIAL_TRANSLATED_CHAPTERS

    def _set_progress(self, percent: int, msg: Optional[str] = None) -> None:
        self.progress = max(0, min(100, percent))
        if msg:
            self.message = msg

    def start_translation_task(self) -> None:
        if self.status != TranslationStatus.QUEUED:
            raise ValueError(TranslationTaskErrors.CANNOT_START_FROM_STATUS.format(status=self.status)) 
        self.status = TranslationStatus.IN_PROGRESS
        self._set_progress(0, "Started")

    def update_progress(self, percent: int, msg: Optional[str] = None, translated_chapters: Optional[int] = None) -> None:
        if self.status != TranslationStatus.IN_PROGRESS:
            raise ValueError(TranslationTaskErrors.PROGRESS_ONLY_IN_PROGRESS)
        updated_progress = max(self.progress, max(0, min(100, percent)))
        self.progress = updated_progress
        if msg:
            self.message = msg
        if translated_chapters is not None:
            self.translated_chapters = max(self.translated_chapters, translated_chapters)

    def complete_task(self, msg: str = "Completed") -> None:
        if self.status != TranslationStatus.IN_PROGRESS:
            raise ValueError(TranslationTaskErrors.MUST_BE_IN_PROGRESS_BEFORE_DONE)
        self._set_progress(100, msg)
        self.status = TranslationStatus.DONE
    
    def fail(self, msg: str = "Failed") -> None:
        self.status = TranslationStatus.FAILED
        if msg:
            self.message = msg

    def cancel(self, msg: str = "Canceled") -> None:
        if self.status in (TranslationStatus.DONE, TranslationStatus.FAILED):
            raise ValueError(TranslationTaskErrors.CANNOT_CANCEL_FINISHED)
        self.status = TranslationStatus.CANCELED
        if msg:
            self.message = msg

    def reset_progress(self, new_total_chapters: Optional[int] = None, msg: str = "Reset") -> None:
        self.progress = 0
        self.translated_chapters = 0
        if new_total_chapters:
            self.total_chapters = new_total_chapters
        self.status = TranslationStatus.QUEUED
        self.message = msg
    
    def __repr__(self):
        cls = self.__class__.__name__
        total = self.total_chapters if self.total_chapters is not None else "?"
        return (
            f"{cls}(id={self.id!r}, book_id={self.book_id!r}, status={self.status.name}, progress={self.progress}%, "
            f"progress_in_chapters={self.translated_chapters}/{total}, message={self.message!r})"
        )
    
    def __str__(self):
        total = self.total_chapters if self.total_chapters is not None else "?"
        return f"Task {self.id}: {self.status.name} {self.progress}% ({self.translated_chapters}/{total})"