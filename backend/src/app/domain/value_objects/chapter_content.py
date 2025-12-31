from dataclasses import dataclass
from typing import Optional
from app.domain.value_objects.footnotes import FootnoteSet

@dataclass(frozen=True)
class ChapterContent:
    text: str
    footnotes: Optional[FootnoteSet] = None

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}(text={self.text!r}, footnotes={self.footnotes!r})"
    
    @property
    def footnote_count(self) -> int:
        return len(self.footnotes) if self.footnotes else 0

    def __str__(self) -> str:
        return f"ChapterContent(text_len={len(self.text)}, footnotes_count={self.footnote_count})"