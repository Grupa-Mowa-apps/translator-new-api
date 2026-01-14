from pydantic import BaseModel
from typing import Optional

class ChapterResponse(BaseModel):
    id: str
    book_id: str
    chapter_number: int
    title: str
    parent_id: Optional[str] = None
    content: Optional[str] = None