from pydantic import BaseModel

class ChapterResponse(BaseModel):
    id: str
    book_id: str
    chapter_number: int
    title: str
    parent_id: str | None = None
    content: str | None = None