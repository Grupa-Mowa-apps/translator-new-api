from pydantic import BaseModel
from typing import Optional, List
from app.application.dto.chapter_dto import ChapterResponse
from app.domain.value_objects.quotation_marks import QuoteType
from app.domain.value_objects.book_status import BookStatus

class CreateBookRequest(BaseModel):
    owner_id: str
    title: str
    genre: str
    quotation_marks: QuoteType
    file_id: Optional[str] = None

class UpdateBookRequest(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    quotation_marks: Optional[QuoteType] = None
    file_id: Optional[str] = None
    status: Optional[BookStatus] = None
    version: Optional[int] = None

class BookResponse(BaseModel):
    id: str
    owner_id: str
    title: str
    genre: str
    quotation_marks: QuoteType
    file_id: Optional[str] = None
    status: str
    version: int

class ProcessBookRequest(BaseModel):
    book_id: str

class BookWithChaptersResponse(BaseModel):
    id: str
    owner_id: str
    title: str
    genre: str
    quotation_marks: str
    file_id: Optional[str] = None
    status: str
    version: int
    chapters: List[ChapterResponse]