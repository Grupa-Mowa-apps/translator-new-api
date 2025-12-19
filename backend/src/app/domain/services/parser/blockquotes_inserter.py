from dataclasses import dataclass
import re
# from app.domain.constants import MARKDOWN_UNESCAPE_RE

MARKDOWN_SPECIAL_CHARS = r"\\[\]\(\)*_{}~`>#+\-.!|="
MARKDOWN_UNESCAPE_RE = re.compile(rf"\\([{MARKDOWN_SPECIAL_CHARS}])")

def _unescape_md(text: str) -> str:
    """
    Removes backslash escapes used in Markdown for special characters.

    Args:
        text(str): Text to be processed.
    Returns:
        str: Processed text.
    """
    return MARKDOWN_UNESCAPE_RE.sub(r"\1", text)

def _normalize_blockquote_key(text: str) -> str:
    """
    Normalizes blockquote content by stripping, hyphenating, deleting * and **, unescaping markdown backslashes,
    merging whitespace into a single space and converting to lowercase.

    Args:
        text(str): Text to be normalized.
    Returns:
        str: Normalized text.
    """
    text = (text or "").strip()
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)
    text = re.sub(r"(\w)-(\w)", r"\1\2", text)
    text = re.sub(r"\*\*([^\*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^\*]+)\*", r"\1", text)
    text = _unescape_md(text)
    text = re.sub(r"\s+", " ", text)
    return text.lower()

@dataclass(frozen=True)
class _BlockReplacement:
    start_idx: int
    end_idx: int
    translation: str
    original_key: str
    original_text: str

def _split_paragraphs(markdown_text: str) -> list[str]:
    """
    """
    return markdown_text.split("\n\n")

def _build_combinations(paragraphs: list[str], max_n: int = 6) -> list[tuple[str, int, int]]:
    """
    Builds a precomputed list of candidate paragraph windows for blockquote matching.

    Args:
        paragraphs(list[str]): List of Markdown paragraphs (produced by splitting on "\\n\\n").
        max_n(int): Maximum number of consecutive paragraphs to combine into one candidate window.

    Returns:
        list[tuple[str, int, int]: A list of tuples (normalized_text, n, start_idx), where:
          - normalized_text: the result of _normalize_blockquote_key applied to the combined window,
          - n: number of paragraphs in the window,
          - start_idx: starting paragraph index of the window in paragraphs.
    """
    paragraph_windows: list[tuple[str, int, int]] = []
    total = len(paragraphs)

    for n in range(1, max_n + 1):
        if total - n < 0:
            break
        for start_idx in range(0, total - n + 1):
            combined = "\n\n".join(paragraphs[start_idx : start_idx + n])
            paragraph_windows.append((_normalize_blockquote_key(combined), n, start_idx))

    return paragraph_windows

def _find_blockquote_replacements(
    markdown_text: str,
    translations: dict[str, str],
    max_paragraphs: int = 6,
) -> list[_BlockReplacement]:
    """
    Finds multi-paragraph blockquote matches in Markdown and return planned paragraph-range replacements.

    Args:
        markdown_text(str): Full markdown text.
        translations(dict[str, str]): Mapping of PL_blockquote -> EN_blockquote (raw strings; normalization happens inside).
        max_paragraphs(int): Maximum number of consecutive paragraphs considered as one candidate blockquote.
    Returns:
        list[_BlockReplacement]: A list of _BlockReplacement objects sorted by start. Each replacement specifies a paragraph
        range [start_idx, end_idx) to be replaced by the English translation.
    """
    paragraphs = _split_paragraphs(markdown_text)
    paragraph_windows = _build_combinations(paragraphs, max_n=max_paragraphs)

    normalized_translations: dict[str, tuple[str, str]] = {}
    for pl_blockquote, en_blockquote in translations.items():
        if not pl_blockquote or not en_blockquote:
            continue
        normalized_key = _normalize_blockquote_key(pl_blockquote)
        normalized_translations[normalized_key] = (pl_blockquote, en_blockquote)

    if not normalized_translations:
        return []

    used_paragraph_indices: set[int] = set()
    planned_replacements: list[_BlockReplacement] = []

    for pl_norm_key, (pl_original, en_translation) in normalized_translations.items():
        for md_window_norm, window_size, start_idx in paragraph_windows:
            if any(idx in used_paragraph_indices for idx in range(start_idx, start_idx + window_size)):
                continue

            if md_window_norm.startswith(pl_norm_key):
                planned_replacements.append(
                    _BlockReplacement(
                        start_idx=start_idx,
                        end_idx=start_idx + window_size,
                        translation=en_translation,
                        original_key=pl_norm_key,
                        original_text=pl_original,
                    )
                )

                for idx in range(start_idx, start_idx + window_size):
                    used_paragraph_indices.add(idx)

                break

    planned_replacements.sort(key=lambda r: r.start_idx)
    return planned_replacements

def _apply_blockquote_replacements(markdown_text: str, replacements: list[_BlockReplacement]) -> str:
    """
    Applies planned blockquote replacements at the paragraph level.

    Args:
        markdown_text(str): Full Markdown document to modify.
        replacements(list[_BlockReplacement]): List of _BlockReplacement objects describing paragraph-range replacements.
    Returns:
        str: Updated Markdown text with all replacement ranges swapped for their translations.
    """
    if not replacements:
        return markdown_text

    paragraphs = _split_paragraphs(markdown_text)

    result: list[str] = []
    i = 0
    replacement_idx = 0

    while i < len(paragraphs):
        if replacement_idx < len(replacements) and i == replacements[replacement_idx].start_idx:
            replacement = replacements[replacement_idx]
            result.append(replacement.translation)
            i = replacement.end_idx
            replacement_idx += 1
            continue

        if paragraphs[i].strip():
            result.append(paragraphs[i])
        i += 1

    return "\n\n".join(result)

def apply_blockquotes_translations(
    markdown_text: str,
    translations: dict[str, str],
    max_paragraphs: int = 6,
) -> str:
    """
    Applies blockquote translations to a markdown document.

    Args:
        markdown_text(str): Full markdown text.
        translations(dict[str, str]): A dictionary with (original polish blockquote) -> english blockquote.
        max_paragraph(int): Maximum number of consecutive paragraphs that may form a single blockquote.
    Returns:
        str: The updated Markdown text with all matched blockquotes replaced by their translations.
    """
    if not translations:
        return markdown_text

    replacements = _find_blockquote_replacements(
        markdown_text=markdown_text,
        translations=translations,
        max_paragraphs=max_paragraphs,
    )
    return _apply_blockquote_replacements(markdown_text, replacements)

def apply_blockquotes_translations_with_report(
    markdown_text: str,
    translations: dict[str, str],
    max_paragraphs: int = 6,
) -> tuple[str, list[dict], list[dict]]:
    """
    Applies blockquote translations to markdown text and return a success/failure report.

    Args:
        markdown_text(str): Full markdown text.
        translations(dict[str, str]): A dictionary with (original polish blockquote) -> english blockquote.
        max_paragraphs(int): Maximum number of consecutive paragraphs that may form a single blockquote.
    Returns:
        tuple[str, list[dict], list[dict]]: A tuple with updated markdown text with translated blockquote contents inserted,
        a list with blockquotes that were successfully inserted into the text and a list with blockquotes that failed to be inserted.
    """
    if not translations:
        return markdown_text, [], []

    normalized_translation_pairs: dict[str, tuple[str, str]] = {}
    for pl_text, en_text in translations.items():
        if not pl_text or not en_text:
            continue
        normalized_key = _normalize_blockquote_key(pl_text)
        normalized_translation_pairs[normalized_key] = (pl_text, en_text)

    replacements = _find_blockquote_replacements(
        markdown_text=markdown_text,
        translations=translations,
        max_paragraphs=max_paragraphs,
    )
    updated_markdown = _apply_blockquote_replacements(markdown_text, replacements)

    applied_normalized_keys = {r.original_key for r in replacements}

    successful = [
        {"type": "blockquote", "original_text": pl, "translation": en, "occurrences": 1}
        for norm_key, (pl, en) in normalized_translation_pairs.items()
        if norm_key in applied_normalized_keys
    ]
    failed = [
        {"type": "blockquote", "original_text": pl, "translation": en}
        for norm_key, (pl, en) in normalized_translation_pairs.items()
        if norm_key not in applied_normalized_keys
    ]

    return updated_markdown, successful, failed