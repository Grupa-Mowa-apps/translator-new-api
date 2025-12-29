from pydantic import BaseModel

from app.domain.value_objects.quotation_marks import QuoteType

class ExportParserRequest(BaseModel):
    quote_type: QuoteType
    excel_filename: str | None = None

class ExportParserResponse(BaseModel):
    excel_path: str
    footnotes_count: int
    quotes_count: int
    blockquotes_count: int

class ApplyParserTranslationsRequest(BaseModel):
    excel_path: str
    output_md_filename: str | None = None

class ApplyParserTranslationsResponse(BaseModel):
    output_md_path: str