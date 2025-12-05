from mrkdwn_analysis import MarkdownAnalyzer
import os

from app.domain.ports.markdown_analyzer import MarkdownAnalyzerPort
from app.domain.errors import FileErrors

class MarkdownAnalyzerAdapter(MarkdownAnalyzerPort):
    def __init__(self, file_path: str):
        self._analyzer = MarkdownAnalyzer(file_path=file_path)
        self._file_path = file_path

    def load_text(self) -> str:
        if not os.path.exists(self._file_path):
            raise ValueError(f"{FileErrors.FILE_NOT_FOUND}: {self._file_path}")
        
        with open(file=self._file_path, mode="r", encoding="utf-8") as file:
            text = file.read()

        return text
    
    def identify_headers(self) -> list[dict[str, any]]:
        raw_headers = self._analyzer.identify_headers()
        headers = raw_headers.get("Header", raw_headers)
        return headers
    
    def identify_footnotes(self) -> list[dict[str, any]]:
        footnotes = self._analyzer.identify_footnotes()
        return footnotes
    
        
    