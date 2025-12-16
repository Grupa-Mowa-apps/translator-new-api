from enum import Enum

class FileKind(str, Enum):
    MARKDOWN = "markdown"
    XLSX = "xlsx"
    TRANSLATED_MARKDOWN = "translated_md"