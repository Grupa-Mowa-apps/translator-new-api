from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class Footnote:
    id: str
    text: str

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}(id={self.id!r}, text={self.text!r})"
    
    def __str__(self):
        return f"[^{self.id}]: {self.text}"

@dataclass(frozen=True)
class FootnoteSet:
    items: List[Footnote]
    
    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}(count={len(self)}, items={self.items!r})"
    
    def __str__(self):
        header = f"Footnotes({len(self)}):"
        body = "\n".join(f" {str(f)}" for f in self.items)
        return header + ("\n" + body if body else "")