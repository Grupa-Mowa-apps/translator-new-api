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

def find_quotes_in_paragraph(paragraph: str, quote_type: QuoteType) -> list[str]:
    """
    Creates a list of quotes as strings for all found quotation marks (together with the quotation marks) in a paragraph.

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

def find_quotes_in_text(paragraphs: list[str], quote_type: QuoteType) -> list[str]:
    """
    Creates a list of quotes as strings for all found quotation marks (together with the quotation marks) in a text (list of paragraphs).

    Args:
        paragraphs(list[str]): List of paragraphs (text) we are searching for quotations in.
        quote_type(QuoteType): Types of quotes that are used in the text - French (« ») or German (» «).

    Returns:
        list[str]: List of quotes as strings together with the quotation marks.
    """

    all_quotes = []

    for paragraph in paragraphs:
        all_quotes.extend(find_quotes_in_paragraph(paragraph=paragraph, quote_type=quote_type))

    return all_quotes

def remove_quotes_from_paragraph(paragraph: str, quote_list: list[str], quote_type: QuoteType, start_index: int=0) -> tuple[str, dict, int]:
    """
    Removes, and replaces with code, quotes from a paragraph so that they will not be visible for the LLM.

    Args:
        paragraph(str): Paragraph in which we are looking for the quotes.
        quote_list(list[str]): List of quotes we are searching for.
        quote_type(QuoteType): Types of quotes that are used in the text - French (« ») or German (» «).
        start_index(int): The number of quote we start counting from.

    Returns:
        tuple[str, dict, int]: Returns a tuple with updated paragraphs with codes instead of quotes, a dictionary with 
        codes and their corresponding quotes and the number of quotes taken out of the paragraph.
    """

    quotes_dict = {}
    updated_paragraph = paragraph
    quote_counter = start_index

    quotes_in_paragraph = find_quotes_in_paragraph(paragraph=paragraph, quote_type=quote_type)
    for quote in quotes_in_paragraph:
        quote_counter += 1
        quote_text = quote[1:-1].strip()
        if quote in quote_list:
            code = f'QUOTE {quote_counter}'
            quotes_dict[code] = quote_text

            escaped_quote = re.escape(quote_text)
            updated_paragraph = re.sub(escaped_quote, f'{code}', updated_paragraph)
    return (updated_paragraph, quotes_dict, quote_counter)

def remove_quotes_from_text(paragraphs: list[str], quote_list: list[str], quote_type: QuoteType) -> tuple[list[str], dict]:
    """
    Removes, and replaces with code, quotes from a list of paragraphs so that they will not be visible for the LLM.

    Args:
        paragraphs(list[str]): List of paragraphs in which we are looking for the quotes.
        quote_list(list[str]): List of quotes we are searching for.
        quote_type(QuoteType): Types of quotes that are used in the text - French (« ») or German (» «).

    Returns:
        tuple[str, dict, int]: Returns a tuple with updated paragraphs with codes instead of quotes, a dictionary with 
        codes and their corresponding quotes and the number of quotes taken out of the paragraph.
    """

    quotes_dict = {}
    updated_paragraphs = []
    quote_counter = 0

    for paragraph in paragraphs:
        updated_paragraph, paragraph_quotes_dict, quote_counter = remove_quotes_from_paragraph(
            paragraph=paragraph,
            quote_list=quote_list,
            quote_type=quote_type,
            start_index=quote_counter
        )
        updated_paragraphs.append(updated_paragraph)
        quotes_dict.update(paragraph_quotes_dict)

    return (updated_paragraphs, quotes_dict)

def insert_quotes_to_paragraph(no_quotes_paragraph: str, quotes_dict: dict) -> str:
    """
    Inserts quotes into a paragraph based on quotes dictionary.

    Args:
        no_quotes_paragraph(str): A paragraph with removed quotes and with codes insted.
        quotes_dict(dict): A dictionary with codes and their corresponding quotes and the number of quotes taken out of the 
        paragraph.

    Returns:
        str: Paragraph with inserted quotes.
    """
    result_paragraph = no_quotes_paragraph

    for code, quote_text in quotes_dict.items():
        code_pattern = re.escape(f'{code}')
        result_paragraph = re.sub(code_pattern, quote_text, result_paragraph)

    return result_paragraph

def insert_quotes_to_text(no_quotes_paragraphs: list[str], quotes_dict: dict) -> list[str]:
    """
    Inserts quotes into a text (list of paragraphs) based on quotes dictionary.

    Args:
        no_quotes_paragraphs(str): A list of paragraph with removed quotes and with codes insted.
        quotes_dict(dict): A dictionary with codes and their corresponding quotes and the number of quotes taken out of the 
        paragraph.

    Returns:
        str: List of paragraphs with inserted quotes.
    """
    result = []

    for paragraph in no_quotes_paragraphs:
        result.append(insert_quotes_to_paragraph(no_quotes_paragraph=paragraph, quotes_dict=quotes_dict))

    return result