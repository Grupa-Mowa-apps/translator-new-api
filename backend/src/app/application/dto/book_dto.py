from pydantic import BaseModel
from app.domain.value_objects.quotation_marks import QuoteType
from app.domain.value_objects.book_status import BookStatus

class CreateBookRequest(BaseModel):
    owner_id: str
    title: str
    genre: str
    quotation_marks: QuoteType
    file_id: str | None = None

class UpdateBookRequest(BaseModel):
    title: str | None = None
    genre: str | None = None
    quotation_marks: QuoteType | None = None
    file_id: str | None = None
    status: BookStatus | None = None
    version: int | None = None

class BookResponse(BaseModel):
    id: str
    owner_id: str
    title: str
    genre: str
    quotation_marks: QuoteType
    file_id: str | None = None
    status: str
    version: int