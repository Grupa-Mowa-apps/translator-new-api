from enum import Enum

class FileKind(str, Enum):
    MARKDOWN ="markdown"
    XLSX = "xlsx"
    TRANSALTED_MARKDOWN = "translated_md"