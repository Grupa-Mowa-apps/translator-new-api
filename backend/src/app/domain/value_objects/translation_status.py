from enum import Enum

class TranslationStatus(str, Enum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELED = "canceled"
    FAILED = "failed"