from dataclasses import dataclass
from typing import Optional
from app.domain.value_objects.footnotes import FootnoteSet

@dataclass(frozen=True)
class ChapterContent:
    text: str
    footnotes: Optional[FootnoteSet] = None

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}(text={self.text!r}, footnotes={self.footnotes!r})"
    
    def __str__(self):
        count = len(self.footnotes) if self.footnotes else 0
        return f"ChapterContent(len(text))={len(self.text)}, footnotes(len(footnotes))={count}"