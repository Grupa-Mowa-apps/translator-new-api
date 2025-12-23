import re
from dataclasses import dataclass

def _clean_md_text(markdown_text: str) -> str:
    """
    Removes backslashes before special markdown characters and trims whitespace at the ends.

    Args:
        markdown_text(str): Full markdown text.
    Returns:
        str: Processed text.
    """
    markdown_text = " ".join(markdown_text.split())
    return re.sub(r'\\([\\[\]\(\)*_{}~`>#+\-.!|=])', r"\1", markdown_text.strip())

def _clean_footnote_translations_keys(
    translations: dict[tuple[str, str], str],
) -> dict[tuple[str, str], str]:
    """
    Normalizes translation keys to match inserter matching (id -> str(int), content -> _clean_md_text).
    
    Args:
        translations(dict[tuple[str, str], str]): Original dictionary with footnotes translations.
    Returns:
        dict[tuple[str, str], str]: Normalized dictionary with footnotes translations.
    """
    return {
        (str(int(footnote_id)), _clean_md_text(pl_text)): en_text
        for (footnote_id, pl_text), en_text in translations.items()
        if footnote_id and pl_text and en_text
    }

def _replace_footnote_match(match: re.Match, translations: dict[tuple[str, str], str]) -> str:
    """
    Returns a new or original footnote definition, depending on whether a translation exists in translations.

    Args:
        match(re.Match): Match for a single footnote definition in Markdown.
        translations(dict[tuple[str, str], str]): A dictionary with keys (footnote_id, original content) -> english content.
    Returns:
        str: Footnote replaced with the translated version if it exists in translations, otherwise the original.
    """

    footnote_id = str(int(match.group(1)))
    content_pl = _clean_md_text(match.group(2))
    translated = translations.get((footnote_id, content_pl))

    if translated:
        return f"[^{footnote_id}]: {translated}"
    
    return match.group(0)


def apply_footnotes_translations(markdown_text: str, translations: dict[tuple[str, str], str]) -> str:
    """
    Applies footnotes translations by replacing existing footnotes in the markdown content with translated ones.

    Args:
        markdown_text(str): Full markdown text.
        translations(dict[tuple[str, str], str]): A dictionary with keys (footnote_id, original content) -> english content.
    Returns:
        str: Text with replaced original footnotes with the translated ones.
    """
    if not translations:
        return markdown_text
    
    translations = _clean_footnote_translations_keys(translations=translations)

    footnote_pattern = re.compile(r"^\[\^(\d+)\]:[ \t]*(.*?)(?=\n\[\^\d+\]:|\Z)", re.MULTILINE | re.DOTALL)

    return re.sub(
        footnote_pattern,
        lambda m: _replace_footnote_match(match=m, translations=translations),
        markdown_text,
    )

@dataclass(frozen=True)
class _FootnoteOccurrance:
    start: int
    end: int
    footnote_id: str
    content_pl_clean: str
    translation: str

def apply_footnotes_translations_with_report(markdown_text: str, translations: dict[tuple[str, str], str]) -> tuple[str, list[dict], list[dict]]:
    """
    Applies footnotes translations to markdown text and returns a success/failure report.

    Args:
        markdown_text(str): Full markdown text.
        translations(dict[tuple[str, str], str]): A dictionary with keys (footnote_id, original content) -> english content.
    Returns:
        tuple[str, list[dict], list[dict]]: A tuple with updated markdown text with translated footnotes inserted,
        a list with footnotes that were successfully inserted into the text and a list with footnotes that failed to be inserted.
    """ 
    if not translations:
        return markdown_text, [], []
    
    translations = _clean_footnote_translations_keys(translations=translations)
    
    footnote_pattern = re.compile(r"^\[\^(\d+)\]:[ \t]*(.*?)(?=\n\[\^\d+\]:|\Z)", re.MULTILINE | re.DOTALL)

    occurrences = []
    for match in re.finditer(footnote_pattern, markdown_text):
        footnote_id = str(int(match.group(1)))
        content_pl_clean = _clean_md_text(match.group(2))

        translated = translations.get((footnote_id, content_pl_clean))
        if not translated:
            continue

        occurrences.append(
            _FootnoteOccurrance(
                start=match.start(),
                end=match.end(),
                footnote_id=footnote_id,
                content_pl_clean=content_pl_clean,
                translation=translated,
            )
        )

    updated_markdown = markdown_text
    for occ in sorted(occurrences, key=lambda x: x.start, reverse=True):
        replacement_text = f"[^{occ.footnote_id}]: {occ.translation}"
        updated_markdown = (
            updated_markdown[: occ.start] + replacement_text + updated_markdown[occ.end :]
        )

    counts = {}
    for occ in occurrences:
        key = (occ.footnote_id, occ.content_pl_clean)
        if key in counts:
            eng_prev, count_prev = counts[key]
            counts[key] = (eng_prev, count_prev + 1)
        else:
            counts[key] = (occ.translation, 1)

    print(counts)

    successful = [
        {
            "type": "footnote",
            "footnote_id": footnote_id,
            "original_text": content_pl_clean,
            "translation": eng_text,
            "occurences": count,
        }
        for (footnote_id, content_pl_clean), (eng_text, count) in counts.items()
    ]

    successful_keys = set(counts.keys())
    failed = [
        {
            "type": "footnote",
            "footnote_id": footnote_id,
            "original_text": pl_text,
            "translation": eng_text,
        }
        for (footnote_id, pl_text), eng_text in translations.items()
        if (footnote_id, _clean_md_text(pl_text)) not in successful_keys
    ]

    return updated_markdown, successful, failed