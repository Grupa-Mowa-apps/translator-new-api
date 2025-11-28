import re

def process_underline_tags(text: str) -> str:
    """
    Deletes underline tags (<u>...</u>) where there are no slashes. SeniorEditor (agent) marks with slashes its better translations.

    Args:
        text(str): Text we want to process.
    Returns:
        str: Processed text.
    """

    underline_pattern = re.compile(r"<u>(.*?)</u>")
    matches = underline_pattern.findall(string=text)

    processed_text = text
    for match in matches:
        if '/' not in match:
            processed_text = processed_text.replace(f'<u>{match}</u>', match)
    
    return processed_text

def normalize_md_breaks_and_punctuation(paragraphs: list[str]) -> list[str]:
    """
    Prepares paragraphs for markdown:
    - adds two spaces at the end of a paragraph if it is not a first or last paragraph nor it is next to an empty line
    (so that the new line character works in md),
    - empty paragraphs remain the same,
    - changes a long pause into a half-pause,
    - replaces [...] with an ellipsis.

    Args:
        list(str): A list of paragraphs.

    Returns:
        list(str): Processed list of paragraphs.
    """

    processed_paragraphs = []
    n = len(paragraphs)

    for i, paragraph in enumerate(paragraphs):
        if paragraph.strip() == "":
            processed_paragraphs.append(paragraph)
        else:
            paragraph = paragraph.replace("—", " – ")
            paragraph = paragraph.replace("[...]", "…")

            first_paragraph_or_previous_empty = (i == 0) or (paragraphs[i - 1].strip() == "")
            last_paragraph_or_next_paragraph_empty = (i == n - 1) or (paragraphs[i + 1].strip() == "")
            if not (first_paragraph_or_previous_empty or last_paragraph_or_next_paragraph_empty):
                print(paragraph)
                paragraph = paragraph.rstrip()
                paragraph += "  "
            processed_paragraphs.append(paragraph)

    return processed_paragraphs
                

