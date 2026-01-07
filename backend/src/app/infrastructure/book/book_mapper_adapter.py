from typing import Callable, Optional
from app.domain.ports.book_mapper_port import BookMapperPort
from app.domain.ports.markdown_analyzer import MarkdownAnalyzerPort


class BookMapperAdapter(BookMapperPort):
    def __init__(self, md_analyzer_factory: Callable[[str], MarkdownAnalyzerPort]):
        self.md_analyzer_factory = md_analyzer_factory

    def map_chapters(self, file_path: str) -> list[dict[str, any]]:
        md_analyzer = self.md_analyzer_factory(file_path)

        markdown_text = md_analyzer.load_text()
        raw_headers = md_analyzer.identify_headers(markdown_text=markdown_text)
        headers = self._normalize_headers(raw_headers=raw_headers)

        headers.sort(key=lambda x: x["start"])

        chapters = []
        number = 0
        last_number_by_level = {}

        for i, header in enumerate(headers):
            number += 1
            level = int(header.get("level", 1))
            title = str(header.get("title", "")).strip()

            start_body = header["end"]
            end_body = headers[i + 1]["start"] if i + 1 < len(headers) else len(markdown_text)
            body = markdown_text[start_body : end_body].strip()

            parent_number = self._compute_parent_number(level=level, last_number_by_level=last_number_by_level)

            chapters.append(
                {
                    "number": number,
                    "title": title,
                    "level": level,
                    "parent_number": parent_number,
                    "text": body,
                }
            )

            last_number_by_level[level] = number
            self._drop_deeper_levels(last=last_number_by_level, level=level)

        return chapters
    
    def map_footnotes(self, file_path: str) -> list[dict[str, any]]:
        md_analyzer = self.md_analyzer_factory(file_path)
        markdown_text = md_analyzer.load_text()
        raw_footnotes = md_analyzer.identify_footnotes(markdown_text=markdown_text) or []
        return raw_footnotes if isinstance(raw_footnotes, list) else []

    def _normalize_headers(self, raw_headers: dict[str, any]) -> list[dict[str, any]]:
        if isinstance(raw_headers, dict):
            return raw_headers.get("Header", raw_headers.get("Headers", []))
        if isinstance(raw_headers, list):
            return raw_headers
        return []
    
    def _compute_parent_number(self, level: int, last_number_by_level: dict[int, int]) -> Optional[int]:
        for parent_level in range(level - 1, 0, -1):
            if parent_level in last_number_by_level:
                return last_number_by_level[parent_level]
        return None
    
    def _drop_deeper_levels(self, last: dict[int, int], level: int) -> None:
        for k in list(last.keys()):
            if k > level:
                last.pop(k, None)