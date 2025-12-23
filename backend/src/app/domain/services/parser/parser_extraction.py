import re
from app.domain.services.quotes_processing import find_quotes_matches
from app.domain.value_objects.quotation_marks import QuoteType
from app.domain.constants import BIBLIO_HEADER_RE

def build_footnotes_dict(footnotes_raw: list[dict[str, str]]) -> dict[str, str]:
    """
    Creates a dictionary {footenote_id -> footnote content} based on raw data from the MarkdownAnalyzer.

    Args:
        footnotes_raw(list[dict[str, str]]): A raw list of dictionaries from the MarkdownAnalyzer representing footnotes.

    Returns:
        dict[str, str]: A dictionary {footenote_id -> footnote content}.
    """

    return {
        f["id"]: re.sub(r'\\([\\[\]\(\)*_{}~`>#+\-.!|=])', r"\1", f["content"])
        for f in footnotes_raw
    }

def cut_text_before_bibliography(markdown_text: str, headers: list[dict[str, any]]) -> str:
    """
    Cuts the text so that it does not contain bibliography.

    Args:
        markdown_text(str): Full markdown text.
        headers(list[dict[str, any]]): List of headers returned by the MarkdownAnalyzer.

    Returns:
        str: Markdown text without the last header.
    """

    if not headers:
        return markdown_text
    
    lines = markdown_text.splitlines()

    for h in headers:
        title = (h.get("text") or "").strip()
        if BIBLIO_HEADER_RE.search(title):
            cutoff_line = h["line"]
            return "\n".join(lines[: cutoff_line - 1])
    
    return markdown_text

def _normalize_headers(raw_headers: dict[str, any]) -> list[dict[str, any]]:
    """
    Normalizes the headers structure returned by MarkdownAnalyzer into a single, consistent list of header
    dictionaries.

    Args:
        raw_headers(dict[str, any]): Dict of headers returned by the MarkdownAnalyzer.

    Returns:
        list[dict[str, any]]: Normalized list of headers.
    """
    if isinstance(raw_headers, dict):
        return raw_headers.get("Header", raw_headers.get("Headers", []))
    if isinstance(raw_headers, list):
        return raw_headers
    return []

def extract_quotes_with_related_footnotes(
        markdown_text: str,
        headers: dict[str, any],
        quote_type: QuoteType,
        footnotes_dict: dict[str, str],
) -> tuple[list[str], list[str]]:
    """
    Retrieves quotes and related footnote (if it follows immediately after the quotation) 
    from the markdown text (excluding the bibliography).

    Args:
        markdown_text(str): Full markdown text.
        headers(list[dict[str, any]]): Dict of headers returned by the MarkdownAnalyzer.
        quote_type(QuoteType): Types of quotes that are used in the text - French (« ») or German (» «).
        footnotes_dict(dict[str, str]): Footnotes dictionary {footenote_id -> footnote content}.
    
    Returns:
        tuple[list[str], list[str]]: Tuple with two lists of the same length: list of unique quotes and list of related 
        footnote content (or "" if none).
    """

    norm_headers = _normalize_headers(raw_headers=headers)

    text_no_biblio = cut_text_before_bibliography(markdown_text=markdown_text, headers=norm_headers)

    all_quotes = []
    footnote_for_quotes = []

    paragraphs = re.split(r"\n\s*\n", text_no_biblio)

    for para in paragraphs:
        for match in find_quotes_matches(paragraph=para, quote_type=quote_type):
            quote_text = match.group(1).strip()
            quote_text = re.sub(r'\\([\\[\]\(\)*_{}~`>#+\-.!|=])', r"\1", quote_text)

            end_idx = match.end()
            is_footnote = re.match(
                r"^[\s\.,;:!\?\)\]\}”’\"…-]*\[\^(\d+)\]",
                para[end_idx:]
            )
            if is_footnote:
                footnote_id = is_footnote.group(1)
                footnote_content = footnotes_dict.get(footnote_id, "")
                all_quotes.append(quote_text)
                footnote_for_quotes.append(footnote_content)
            else:
                all_quotes.append(quote_text)
                footnote_for_quotes.append("")

    unique_quotes = {}
    for quote, footnote in zip(all_quotes, footnote_for_quotes):
        if quote not in unique_quotes:
            unique_quotes[quote] = footnote

    final_quotes = []
    related_quotes = []
    for quote, footnote in unique_quotes.items():
        if not any(quote != other and quote in other for other in unique_quotes):
            final_quotes.append(quote)
            related_quotes.append(footnote)

    return final_quotes, related_quotes

def extract_blockquotes(markdown_text: str) -> list[str]:
    """
    Retrieves blockquotes marked with @@@...@@@, removes backslashes and duplicates while preserving order.

    Args:
        markdown_text(str): Full markdown text.

    Returns:
        list[str]: List of retrieved unique blockquotes.
    """

    blockquote_pattern = re.compile(r"@@@(.*?)@@@", re.DOTALL)
    matches = blockquote_pattern.findall(markdown_text)

    cleaned_quotes = []
    for quote in matches:
        quote = quote.strip()
        quote = re.sub(r'\\([\\[\]\(\)*_{}~`>#+\-.!|=])', r"\1", quote)
        cleaned_quotes.append(quote)

    seen_blockquotes = set()
    unique_blockquotes = []
    for quote in cleaned_quotes:
        if quote not in seen_blockquotes:
            seen_blockquotes.add(quote)
            unique_blockquotes.append(quote)

    return unique_blockquotes
