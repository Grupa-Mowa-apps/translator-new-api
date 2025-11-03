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
    
    def _footnote_count(self):
        return len(self.footnotes) if self.footnotes else 0

    def __str__(self):  
        return f"ChapterContent(len(text))={len(self.text)}, footnotes(len(footnotes))={self._footnote_count()}"