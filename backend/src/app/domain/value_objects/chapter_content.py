from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class ChapterContent:
    text: str
    footnotes_md: Optional[str] = None

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}(text={self.text!r}, footnotes_md={self.footnotes_md!r})"
    
    def __str__(self):
        return f"ChapterContent: {self.text}, {self.footnotes_md}"