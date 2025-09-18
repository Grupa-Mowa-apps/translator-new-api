from dataclasses import dataclass
from typing import Optional
from domain.value_objects.translation_status import TranslationStatus

@dataclass
class TranslationTask:
    id: str   # task_id SSE
    book_id: str
    status: TranslationStatus = TranslationStatus.QUEUED
    progress: int = 0
    message: Optional[str] = None
    total_chapters: Optional[int] = None
    translated_chapters: int = 0

    def _set_progress(self, percent: int, msg: Optional[str] = None) -> None:
        self.progress = max(0, min(100, percent))
        if msg:
            self.message = msg

    def start_translation_task(self) -> None:
        if self.status != TranslationStatus.QUEUED:
            raise ValueError(f"Cannot start from status {self.status}") 
        self.status = TranslationStatus.IN_PROGRESS
        self._set_progress(0, "Started")

    def update_progress(self, percent: int, msg: Optional[str] = None, translated_chapters: Optional[int] = None) -> None:
        if self.status != TranslationStatus.IN_PROGRESS:
            raise ValueError("Progress can be update only when IN_PROGRESS")
        updated_progress = max(self.progress, max(0, min(100, percent)))
        self.progress = updated_progress
        if msg:
            self.message = msg
        if translated_chapters is not None:
            self.translated_chapters = max(self.translated_chapters, translated_chapters)

    def complete_task(self, msg: str = "Completed") -> None:
        if self.status != TranslationStatus.IN_PROGRESS:
            raise ValueError("Must be IN_PROGRESS before DONE")
        self._set_progress(100, msg)
        self.status = TranslationStatus.DONE
    
    def fail(self) -> None:
        self.status = TranslationStatus.FAILED