from enum import Enum

class BookStatus(str, Enum):
    UPLOADED = "uploaded"
    PARSED = "parsed"
    ANNOTATIONS_APPLIED = "annotations_applied"
    READY_TO_TRANSLATE = "ready_to_translate"
    IN_TRANSLATION = "in_translation"
    TRANSLATED = "translated"
    FAILED = "failed"

    def __repr__(self):
        return super().__repr__()
    
    def __str__(self):
        return super().__str__()