from dataclasses import dataclass
from typing import List, Optional
from domain.entities.chapter import Chapter
from domain.value_objects.quotation_marks import QuoteType
from domain.value_objects.book_status import BookStatus
from domain.constants import INITIAL_VERSION
from domain.errors import BookErrors

@dataclass
class Book:
    id: str
    owner_id: str

    title: str
    genre: str
    quotation_marks: QuoteType

    file_path: Optional[str]
    
    chapters: List[Chapter]
    
    status: BookStatus = BookStatus.UPLOADED
    version: int = INITIAL_VERSION

    def _update_version(self) -> None:
        self.version += 1
    
    def rename_title(self, new_title: str) -> None:
        if not new_title or not new_title.strip():
            raise ValueError(BookErrors.TITLE_CANNOT_BE_EMPTY)
        self.title = new_title.strip()
        self._update_version()

    def change_genre(self, new_genre: str) -> None:
        if not new_genre or not new_genre.strip():
            raise ValueError(BookErrors.GENRE_CANNOT_BE_EMPTY)
        self.genre = new_genre.strip()
        self._update_version()

    def change_quotation_marks(self, new_qt: QuoteType) -> None:
        self.quotation_marks = new_qt
        self._update_version()

    def mark_parsed(self) -> None:
        self.status = BookStatus.PARSED
        self._update_version()
    
    def mark_ready_to_translate(self) -> None:
        self.status = BookStatus.READY_TO_TRANSLATE
        self._update_version()

    def start_translation(self) -> None:
        self.status = BookStatus.IN_TRANSLATION
        self._update_version()

    def mark_translated(self) -> None:
        self.status = BookStatus.TRANSLATED
        self._update_version()
    
    def mark_failed(self) -> None:
        self.status = BookStatus.FAILED
        self._update_version()

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return (
            f"{cls}(id={self.id!r}, title={self.title!r}, genre={self.genre!r}, status={self.status.name}, "
            f"version={self.version}, chapters={len(self.chapters)})"
        )
    
    def __str__(self) -> str:
        return f"{self.title} (v{self.version}, {self.status.name})"
