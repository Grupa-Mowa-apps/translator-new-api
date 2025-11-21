import re
from app.domain.value_objects.quotation_marks import QuoteType
from app.domain.errors import QuoteTypeErrors

def _get_quote_patterns(quote_type: QuoteType) -> list[str]:
    """
    Creates a list of quotation mark patterns for a given language.
    
    Args:
        quote_type(QuoteType): Types of quotes that are used in the text - French (« ») or German (» «).

    Returns:
        list(str): List of quotation mark patterns.
    """

    result = [
        r'"(.*?)"',   # U+0022 - quotation mark - "..."
        r"'(.*?)'",   # U+0027 - apostrophe - '...'
        r'“(.*?)”',   # U+201C + U+201D - left double quotaion mark + right double quotation mark - “...”
        r'„(.*?)”',   # U+201E + U+201D - double low quotation mark + right double quotation mark - „...”
        r'‚(.*?)’',   # U+201A + U+2018 - single low quotation mark + left single quotation mark - ‚...’
        r'‘(.*?)’',   # U+2018 + U+2019 - left single quotation mark + right single quotation mark - ‘...’
        r'‹(.*?)›',   # U+2039 + U+203A - single left-pointing angle quotation mark + wingle right-pointing angle quotation mark - ‹...›
    ]

    if quote_type == QuoteType.FR:
        result.append(r'«(.*?)»')   # U+00AB + U+00BB - left-pointing double angle quotation mark + right-pointing double angle quotation mark - «...»
    elif quote_type == QuoteType.GE:
        result.append(r'»(.*?)«')   # U+00BB + U+00AB - right-pointing double angle quotation mark + left-pointing double angle quotation mark - »...«
    else:
        raise ValueError(QuoteTypeErrors.INVALID_QUOTE_TYPE)

    return result

def find_quotes_matches(paragraph: str, quote_type: QuoteType) -> list[re.Match]:
    """
    Creates a list of re.Match for all found quotes.

    Args:
        paragraph(str): A piece of text searched for quotations.
        quote_type(QuoteType): Types of quotes that are used in the text - French (« ») or German (» «).

    Returns:
        list[re.Match]: List of re.Matches for all found quotes.
    """

    quote_patterns = _get_quote_patterns(quote_type=quote_type)
    matches = []
    for pattern in quote_patterns:
        matches.extend(re.finditer(pattern=pattern, string=paragraph, flags=re.DOTALL))

    matches.sort(key=lambda m: m.start())
    return matches

def find_quotes(paragraph: str, quote_type: QuoteType) -> list[str]:
    """
    Creates a list of quotes as strings for all found quotation marks (together with the quotation marks).

    Args:
        paragraph(str): A piece of text searched for quotations.
        quote_type(QuoteType): Types of quotes that are used in the text - French (« ») or German (» «).

    Returns:
        list[str]: List of quotes as strings together with the quotation marks.
    """    
    matches = find_quotes_matches(paragraph=paragraph, quote_type=quote_type)
    quotes = []

    for match in matches:
        quote = match.group(0).strip()
        quote = re.sub(r'\\([\\[\]\(\)*_{}~`>#+\-.!|=])', r'\1', quote)
        quotes.append(quote)
    return quotes

def remove_quotes_from_paragraph(paragraph: str, quote_list: list[str], quote_type: QuoteType) -> tuple[str, dict]:
    """
    Removes, and replaces with code, quotes from a paragraph so that they will not be visible for the LLM.

    Args:
        paragraph(str): Paragraph in which we are looking for the quotes.
        quote_list(list[str]): List of quotes we are searching for.
        quote_type(QuoteType): Types of quotes that are used in the text - French (« ») or German (» «).

    Returns:
        tuple[str, dict]: 
    """

    quote_dict = {}
    updated_paragraph = paragraph
    quote_counter = 0

    quotes_in_paragraph = find_quotes(paragraph=paragraph, quote_type=quote_type)
    for quote in quotes_in_paragraph:
        quote_counter += 1
        quote_text = quote[1:-1].strip()
        if quote in quote_list:
            code = f'QUOTE {quote_counter}'
            quote_dict[code] = quote_text

            escaped_quote = re.escape(quote_text)
            updated_paragraph = re.sub(escaped_quote, f'"{code}', updated_paragraph)
    return (updated_paragraph, quote_dict)