import re

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
    Replaces existing footnotes in the markdown content with translated ones.

    Args:
        markdown_text(str): Full markdown text.
        translations(dict[tuple[str, str], str]): A dictionary with keys (footnote_id, original content) -> english content.
    Returns:
        str: Text with replaced original footnotes with the translated ones.
    """

    footnote_pattern = re.compile(r"^\[\^(\d+)\]:[ \t]*(.*?)(?=\n\[\^\d+\]:|\Z)", re.MULTILINE | re.DOTALL)

    return re.sub(
        footnote_pattern,
        lambda m: _replace_footnote_match(match=m, translations=translations),
        markdown_text,
    )

def apply_quotes_translations(markdown_text: str, translations: dict[str, str]) -> str:
    """
    Replaces quotes (normal or blockquotes) in markdown with their translations.

    Args:
        markdown_text(str): Full markdown text.
        translations(dict[str, str]): Dictionary with translations {original Polish quote/blockquote} -> {English quote/blockquote}
    Returns:
        str: Text with replaced original quotes with the translated ones.
    """

    text_with_translations = markdown_text
    for original in sorted(translations.keys(), key=len, reverse=True):
        text_with_translations = text_with_translations.replace(original, translations[original])
    return text_with_translations