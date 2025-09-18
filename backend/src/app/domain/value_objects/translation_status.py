from enum import Enum

class TranslationStatus(str, Enum):
    QUEUED = "queued"   # zadanie tlumaczenia zostalo przyjete, stoi w kolejce, ale jeszcze nie wystartowalo
    IN_PROGRESS = "in_progress"
    DONE = "done"
    FAILED = "failed"