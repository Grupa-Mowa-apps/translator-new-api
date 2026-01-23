from typing import Optional
from pydantic import BaseModel

class TranslateBookRequest(BaseModel):
    book_id: str
    translate_all: bool = True
    chapter_ids: Optional[list[str]] = None
    batch_size: int
    output_filename: Optional[str] = None

class TranslateBookResponse(BaseModel):
    book_id: str
    output_path: str
    translated_chapters: int
    status: str