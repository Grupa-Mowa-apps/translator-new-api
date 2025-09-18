from dataclasses import dataclass
from domain.value_objects.quotes_status import QuotesStatus

@dataclass
class QuoteSet:
    id: str
    book_id: str
    version: int = 1
    status: QuotesStatus = QuotesStatus.DRAFT
    file_path: str

    def _update_version(self) -> None:
        self.version += 1

    def mark_extracted(self) -> None:
        self.status = QuotesStatus.EXTRACTED
        self._update_version

    def mark_translated(self) -> None:
        if self.status != QuotesStatus.EXTRACTED:
            raise ValueError("Must be EXTRACTED before TRANSLATED")
        self.status = QuotesStatus.TRANSLATED
        self._update_version

    def mark_reviewed(self) -> None:
        if self.status != QuotesStatus.TRANSLATED:
            raise ValueError("Must be TRANSLATED before REVIEWED")
        self.status = QuotesStatus.REVIEWED
        self._update_version

    def mark_applied(self) -> None:
        if self.status != QuotesStatus.REVIEWED:
            raise ValueError("Must be REVIEWED before APPLIED")
        self.status = QuotesStatus.APPLIED
        self._update_version