from dataclasses import dataclass
from typing import List
from domain.entities.chapter import Chapter
from domain.value_objects.quotation_marks import QuoteType
from domain.value_objects.book_status import BookStatus

@dataclass
class Book:
    id: str
    title: str
    genre: str
    quotation_marks: QuoteType
    owner_id: str
    status: BookStatus = BookStatus.UPLOADED
    file_path: str
    chapters: List[Chapter]
    version: int = 1

    def _update_version(self) -> None:
        self.version += 1
    
    def rename_title(self, new_title: str) -> None:
        if not new_title or not new_title.strip():
            raise ValueError("Title cannot be empty")
        self.title = new_title.strip()
        self._update_version

    def change_genre(self, new_genre: str) -> None:
        if not new_genre or not new_genre.strip():
            raise ValueError("Genre cannot be empty")
        self.genre = new_genre.strip()
        self._update_version

    def change_quotation_marks(self, new_qt: QuoteType) -> None:
        self.quotation_marks = new_qt
        self._update_version

    def mark_parsed(self) -> None:
        self.status = BookStatus.PARSED
        self._update_version
    
    def mark_ready_to_translate(self) -> None:
        self.status = BookStatus.READY_TO_TRANSLATE
        self._update_version

    def start_translation(self) -> None:
        self.status = BookStatus.IN_TRANSLATION
        self._update_version

    def mark_translated(self) -> None:
        self.status = BookStatus.TRANSLATED
        self._update_version
    
    def mark_failed(self) -> None:
        self.status = BookStatus.FAILED
        self._update_version


