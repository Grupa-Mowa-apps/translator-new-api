from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)   # obiekt jest niemodyfikowalny
class ChapterContent:
    # chcemy zeby tekst i przypisy byly oddzielnie
    text: str
    footnotes_md: Optional[str] = None