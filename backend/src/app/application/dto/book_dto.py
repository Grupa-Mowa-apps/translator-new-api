from pydantic import BaseModel

class BookResponse(BaseModel):
    id: str
    title: str
    genre: str