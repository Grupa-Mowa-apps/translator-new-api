import re


INITIAL_VERSION: int = 1
INITIAL_PROGRESS: int = 0
INITIAL_TRANSLATED_CHAPTERS: int = 0
INITIAL_CHAPTER_NUMBER: int = 0

QUOTE_PATTERNS = [
    r'"(.*?)"',
    r"'(.*?)'",
    r'“(.*?)”',
    r'„(.*?)”',
    r'‚(.*?)’',
    r'‘(.*?)’',
    r'«(.*?)»',
    r'»(.*?)«',
    r'‹(.*?)›',
]

MARKDOWN_SPECIAL_CHARS = r"\\[\]\(\)*_{}~`>#+\-.!|="
MARKDOWN_UNESCAPE_RE = re.compile(rf"\\([{MARKDOWN_SPECIAL_CHARS}])")