from dataclasses import dataclass
from typing import Optional
from app.domain.value_objects.file_kind import FileKind
from app.domain.constants import INITIAL_VERSION
from app.domain.errors import FileErrors

@dataclass
class File:
    id: str
    owner_id: str

    kind: FileKind
    path: str
    filename: str

    book_id: Optional[str] = None

    version: int = INITIAL_VERSION

    def _update_version(self) -> None:
        self.version += 1

    def rename(self, new_filename: str) -> None:
        if not new_filename or not new_filename.strip():
            raise ValueError(FileErrors.FILENAME_CANNOT_BE_EMPTY)
        self.filename = new_filename.strip()
        self._update_version()

    def move_to(self, new_path: str) -> None:
        if not new_path or not new_path.strip():
            raise ValueError(FileErrors.PATH_CANNOT_BE_EMPTY)
        self.path = new_path.strip()
        self._update_version()

    def change_owner(self, new_owner_id: str) -> None:
        if not new_owner_id or not new_owner_id.strip():
            raise ValueError(FileErrors.OWNER_ID_CANNOT_BE_EMPTY)
        self.owner_id = new_owner_id.strip()
        self._update_version()

    def attach_to_book(self, book_id: str) -> None:
        if not book_id or not book_id.strip():
            raise ValueError(FileErrors.BOOK_ID_CANNOT_BE_EMPTY)
        self.book_id = book_id
        self._update_version()

    def detach_from_book(self) -> None:
        self.book_id = None
        self._update_version()

    def change_kind(self, new_kind: FileKind) -> None:
        if not isinstance(new_kind, FileKind):
            raise ValueError(FileErrors.INVALID_FILE_KIND)
        self.kind = new_kind

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return (
            f"{cls}(id={self.id!r}, kind={self.kind.name}, filename={self.filename!r}, "
            f"version={self.version})"
        )
    
    def __str__(self) -> str:
        return f"{self.kind.name} {self.filename} v({self.version})"
