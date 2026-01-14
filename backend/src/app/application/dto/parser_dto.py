from pydantic import BaseModel
from typing import Optional
from app.domain.value_objects.quotation_marks import QuoteType

class ExportParserRequest(BaseModel):
    quote_type: QuoteType
    excel_filename: Optional[str] = None

class ExportParserResponse(BaseModel):
    annotation_set_id: str
    excel_path: str
    footnotes_count: int
    quotes_count: int
    blockquotes_count: int

class ApplyParserTranslationsRequest(BaseModel):
    annotation_set_id: str
    output_md_filename: Optional[str] = None

class ApplyParserTranslationsResponse(BaseModel):
    output_md_path: str