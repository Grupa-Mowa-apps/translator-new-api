from enum import Enum

# [CODE REVIEW] [SUGGESTION] Literówka: TRANSALTED_MARKDOWN powinno być TRANSLATED_MARKDOWN
class FileKind(str, Enum):
    MARKDOWN ="markdown"
    XLSX = "xlsx"
    TRANSALTED_MARKDOWN = "translated_md"