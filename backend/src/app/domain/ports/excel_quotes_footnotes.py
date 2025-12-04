from typing import Protocol

from app.domain.value_objects.quotation_marks import QuoteType


class ExcelQuotesFootnotesPort(Protocol):
    def export_from_markdown(self, md_path: str, excel_path: str, quote_type: QuoteType) -> None: ...
    def apply_translations_from_excel(self, excel_path: str, md_input_path: str, md_output_path: str) -> None: ...