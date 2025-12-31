from dataclasses import dataclass
from typing import Optional
from app.domain.value_objects.chapter_content import ChapterContent

@dataclass
class Chapter:
    id: str
    book_id: str
    chapter_number: int
    title: str
    parent_id: Optional[str] = None
    content: Optional[ChapterContent] = None

    def __post_init__(self) -> None:
        if self.chapter_number <= 0:
            raise ValueError("Chapter number must be greater than 0")

    def is_subchapter(self) -> bool:
        return self.parent_id is not None
    
    def rename_title(self, new_title: str) -> None:
        if not new_title or not new_title.strip():
            raise ValueError("Title cannot be empty")
        self.title = new_title.strip()

    def set_parent(self, parent_id: Optional[str]) -> None:
        if parent_id == self.id:
            raise ValueError("Chapter cannot be its own parent")
        self.parent_id = parent_id
    
    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return (
            f"{cls}(id={self.id!r}, chapter_number={self.chapter_number}, title={self.title!r}, book_id={self.book_id!r}, "
            f"parent_id={self.parent_id!r}, has_content={self.content is not None})"
        )
    
    def __str__(self) -> str:
        tag = "Subchapter" if self.parent_id else "Chapter"
        return f"{tag} {self.chapter_number}: {self.title}"