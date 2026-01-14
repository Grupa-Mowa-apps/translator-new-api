from mrkdwn_analysis import MarkdownAnalyzer
import os
import re

from app.domain.ports.markdown_analyzer import MarkdownAnalyzerPort
from app.domain.errors import FileErrors

BOLD_LINE_TO_MD_HEADER = re.compile(r'^\s*\*\*([^\n]+?)\*\*\s*$', re.MULTILINE)
MD_HEADER_RE = re.compile(r'^(#{1,6})\s+(.*\S)\s*$')

class MarkdownAnalyzerAdapter(MarkdownAnalyzerPort):
    def __init__(self, file_path: str):
        self._analyzer = MarkdownAnalyzer(file_path=file_path)
        self._file_path = file_path

    def load_text(self) -> str:
        if not os.path.exists(self._file_path):
            raise ValueError(f"{FileErrors.FILE_NOT_FOUND}: {self._file_path}")
        
        with open(file=self._file_path, mode="r", encoding="utf-8") as file:
            text = file.read()

        text = self._bold_header_lines_to_markdown_header(markdown_text=text)

        return text
    
    def identify_headers(self) -> list[dict[str, any]]:
        # raw_headers = self._analyzer.identify_headers()
        # return raw_headers
        text = self.load_text()
        headers: list[dict[str, any]] = []

        for line_no, line in enumerate(text.splitlines(), start=1):
            m = MD_HEADER_RE.match(line)
            if not m:
                continue
            level = len(m.group(1))
            title = m.group(2).strip()
            headers.append({"line": line_no, "level": level, "text": title})

        return {"Header": headers}
    
    def identify_footnotes(self) -> list[dict[str, any]]:
        footnotes = self._analyzer.identify_footnotes()
        return footnotes
    
    def _bold_header_lines_to_markdown_header(self, markdown_text: str) -> str:
        return BOLD_LINE_TO_MD_HEADER.sub(r'# \1', markdown_text)