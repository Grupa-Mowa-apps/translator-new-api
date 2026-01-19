from enum import Enum

class AnnotationStatus(str, Enum):
    EXTRACTED_FROM_MD_TO_XLSX = "extracted_from_md_to_xlsx"
    TRANSLATED = "translated"
    REVIEWED = "reviewed"
    APPLIED = "applied"