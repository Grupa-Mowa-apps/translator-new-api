from dataclasses import dataclass
import re
from app.domain.constants import QUOTE_PATTERNS, MARKDOWN_UNESCAPE_RE

def _unescape_md(text: str) -> str:
    """
    Removes backslash escapes used in Markdown for special characters.

    Args:
        text(str): Text to be processed.
    Returns:
        str: Processed text.
    """
    return MARKDOWN_UNESCAPE_RE.sub(r"\1", text)

def _normalize_quote_key(text: str) -> str:
    """
    Normalizes quote content by removing whitespaces at the beginning and at the end,
    unescaping Markdown backslashes and converting to lowercase.

    Args:
        text(str): Text to be normalized.
    Returns:
        str: Normalized text.
    """
    text = text.strip()
    text = _unescape_md(text=text)
    return text.lower()

@dataclass(frozen=True)
class _Replacement:
    start: int
    end: int
    replacement: str
    original: str
    translation: str

def _find_quote_replacements(markdown_text: str, translations: dict[str, str]) -> list[_Replacement]:
    """
    Finds all quotes in a markdown text and builds a list of replacements for those that have translations.

    Args:
        markdown_text(str): Full markdown text.
        translations(dict[str, str]):  A dictionary with key (normalized polish quote) -> english quote.
    Returns:
        list[_Replacement]: List of _Replacement objects containing start, end, replacement text, original quote and its translation for reporting purposes.
    """
    replacements = []
    for pattern in QUOTE_PATTERNS:
        for match in re.finditer(pattern=pattern, string=markdown_text, flags=re.DOTALL):
            quoted_text = match.group(1).strip()
            normalized_key = _normalize_quote_key(text=quoted_text)

            translated_quote_text = translations.get(normalized_key)
            if not translated_quote_text:
                continue

            full_match = match.group(0)
            left_quote_mark = full_match[0]
            right_quote_mark = full_match[-1]

            replacement_text = f"{left_quote_mark}{translated_quote_text}{right_quote_mark}"

            replacements.append(_Replacement(
                start=match.start(),
                end=match.end(),
                replacement=replacement_text,
                original=quoted_text,
                translation=translated_quote_text,
            ))
    return replacements

def _apply_quotes_replacements(markdown_text: str, replacements: list[_Replacement]) -> str:
    """
    Applies prepared replacements to markdown text.

    Args:
        markdown_text(str): Full markdown text.
        replacements(list[_Replacement]): List of replacement operations.
    Returns:
        str: Updated markdown text with all replacements applied.
    """
    replacements_sorted = sorted(replacements, key=lambda r: r.start, reverse=True)
    for replacement in replacements_sorted:
        markdown_text = markdown_text[:replacement.start] + replacement.replacement + markdown_text[replacement.end:]
    
    return markdown_text

def apply_quotes_translations(markdown_text: str, translations: dict[str, str]) -> str:
    """
    Applies quote translations to markdown text.

    Args:
        markdown_text(str): Full markdown text.
        translations(dict[str, str]): A dictionary with key (original polish quote) -> english quote.
    Returns:
        str: Updated markdown text with translated quote contents inserted.
    """
    if not translations:
        return markdown_text
    
    normalised_translations = {
        _normalize_quote_key(pl): en
        for pl, en in translations.items()
    }

    replacements = _find_quote_replacements(markdown_text=markdown_text, translations=normalised_translations)
    
    updated_markdown = _apply_quotes_replacements(
        markdown_text=markdown_text,
        replacements=replacements,
    )
    
    return updated_markdown

def apply_quotes_translations_with_report(markdown_text: str, translations: dict[str, str]) -> tuple[str, list[dict], list[dict]]:
    """
    Applies quote translations to markdown text and return a success/failure report.

    Args:
        markdown_text(str): Full markdown text.
        translations(dict[str, str]): A dictionary with key (original polish quote) -> english quote.
    Returns:
        tuple[str, list[dict], list[dict]]: A tuple with updated markdown text with translated quote contents inserted,
        a list with quotes that were successfully inserted into the text and a list with quotes that failed to be inserted.
    """
    if not translations:
        return markdown_text, [], []
    
    normalised_translations = {
        _normalize_quote_key(pl): en
        for pl, en in translations.items()
    }

    replacements = _find_quote_replacements(markdown_text=markdown_text, translations=normalised_translations)
    if not replacements:
        failed = [
            {"type": "quote", "original_text": pl, "translation": en}
            for pl, en in translations.items()
        ]
        return markdown_text, [], failed
    
    updated_markdown = _apply_quotes_replacements(
        markdown_text=markdown_text,
        replacements=replacements,
    )
    
    successful_occurrences = {}
    for replacement in replacements:
        if replacement.original in successful_occurrences:
            eng_prev, count_prev = successful_occurrences[replacement.original]
            successful_occurrences[replacement.original] = (eng_prev, count_prev + 1)
        else:
            successful_occurrences[replacement.original] = (replacement.translation, 1)
    
    successful = [
        {
            "type": "quote",
            "original_text": pl,
            "translation": en,
            "occurences": count,
        }
        for pl, (en, count) in successful_occurrences.items()
    ]

    successful_pl_set = set(_normalize_quote_key(k) for k in successful_occurrences.keys())
    failed = [
        {"type": "quote", "original_text": pl, "translation": en}
        for pl, en in translations.items()
        if _normalize_quote_key(pl) not in successful_pl_set
    ]

    return updated_markdown, successful, failed