from dataclasses import dataclass
from typing import Optional
from domain.value_objects.chapter_content import ChapterContent

@dataclass
class Chapter:
    id: str
    no: int   # np. 1, 2
    title: str
    book_id: str
    parent_id: Optional[str] = None
    content: Optional[ChapterContent] = None

    def is_subchatper(self) -> bool:
        return self.parent_id is not None
    
    def rename_title(self, new_title: str) -> None:
        if not new_title or not new_title.strip():
            raise ValueError("Title cannot be empty")
        self.title = new_title.strip()

    def set_parent(self, parent_id: Optional[str]) -> None:
        if parent_id == self.id:
            raise ValueError("Chapter cannot be its own parent")
        self.parent_id = parent_id