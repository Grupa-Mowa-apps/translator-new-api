from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class Footnote:
    id: str
    text: str
    
    def __post_init__(self) -> None:
        if not self.id or not self.id.strip():
            raise ValueError("Footnote id cannot be empty")
        if not self.text or not self.text.strip():
            raise ValueError("Footnote text cannot be empty")
        object.__setattr__(self, 'id', self.id.strip())
        object.__setattr__(self, 'text', self.text.strip())

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}(id={self.id!r}, text={self.text!r})"
    
    def __str__(self) -> str:
        return f"[^{self.id}]: {self.text}"

@dataclass(frozen=True)
class FootnoteSet:
    items: List[Footnote]
    
    def __post_init__(self) -> None:
        if self.items is None:
            object.__setattr__(self, 'items', [])
        ids = [f.id for f in self.items]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate footnote ids found")
    
    def __len__(self) -> int:
        return len(self.items)

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}(count={len(self)}, items={self.items!r})"
    
    def __str__(self) -> str:
        header = f"Footnotes({len(self)}):"
        body = "\n".join(f" {str(f)}" for f in self.items)
        return header + ("\n" + body if body else "")