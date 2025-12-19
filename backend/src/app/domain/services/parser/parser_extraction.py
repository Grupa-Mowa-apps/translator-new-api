import re
from app.domain.services.quotes_processing import find_quotes_matches
from app.domain.value_objects.quotation_marks import QuoteType

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

def cut_text_before_last_heading(markdown_text: str, headers: list[dict[str, any]]) -> str:
    """
    Cuts the text so that it does not contain bibliography (the last header).

    Args:
        markdown_text(str): Full markdown text.
        headers(list[dict[str, any]]): List of headers returned by the MarkdownAnalyzer.

    Returns:
        str: Markdown text without the last header.
    """

    if not headers:
        return markdown_text
    
    lines = markdown_text.splitlines()
    last_heading = headers[-1]
    cutoff_line = last_heading["line"]
    return "\n".join(lines[: cutoff_line - 1])

def extract_quotes_with_related_footnotes(
        markdown_text: str,
        headers: list[dict[str, any]],
        quote_type: QuoteType,
        footnotes_dict: dict[str, str],
) -> tuple[list[str], list[str]]:
    """
    Retrieves quotes and related footnote (if it follows immediately after the quotation) 
    from the markdown text (excluding the bibliography).

    Args:
        markdown_text(str): Full markdown text.
        headers(list[dict[str, any]]): List of headers returned by the MarkdownAnalyzer.
        quote_type(QuoteType): Types of quotes that are used in the text - French (« ») or German (» «).
        footnotes_dict(dict[str, str]): Footnotes dictionary {footenote_id -> footnote content}.
    
    Returns:
        tuple[list[str], list[str]]: Tuple with two lists of the same length: list of unique quotes and list of related 
        footnote content (or "" if none).
    """

    text_no_biblio = cut_text_before_last_heading(markdown_text=markdown_text, headers=headers)

    quotes_matches = find_quotes_matches(paragraph=markdown_text, quote_type=quote_type)

    all_quotes = []
    footnote_for_quotes = []

    for match in quotes_matches:
        quote_text = match.group(1).strip()
        quote_text = re.sub(r'\\([\\[\]\(\)*_{}~`>#+\-.!|=])', r"\1", quote_text)

        end_idx = match.end()
        is_footnote = re.match(r"\[\^(\d+)\]", text_no_biblio[end_idx:])

        if is_footnote:
            footnote_id = is_footnote.group(1)
            footnote_content = footnotes_dict.get(footnote_id, "")
            all_quotes.append(quote_text)
            footnote_for_quotes.append(footnote_content)
        elif len(quote_text.split()) > 2:
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
