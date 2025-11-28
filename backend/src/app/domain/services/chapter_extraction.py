import re
from typing import Optional
import uuid
from app.domain.entities.chapter import Chapter
from app.domain.value_objects.footnotes import FootnoteSet, Footnote
from app.domain.value_objects.chapter_content import ChapterContent


def _make_all_footnotes(footnotes_raw: list[dict[str, str]]) -> FootnoteSet:
    """
    Converts a raw list of dictionaries into FootnoteSet object.

    Args:
        footnotes_raw(list[dict[str, str]]): A raw list of dictionaries from the MarkdownAnalyzer representing footnotes.

    Returns:
        FootnoteSet: FootnoteSet object - a list of Footnote objects.
    """ 

    items = [Footnote(id=f["id"], text=f["content"]) for f in footnotes_raw]
    return FootnoteSet(items=items)

def _get_chapter_content_by_title(
        markdown_text: str, 
        headers: list[dict[str, any]], 
        all_footnotes: FootnoteSet, 
        chapter_title: str,
        footnotes_start_line: Optional[int] = None,
    ) -> ChapterContent:
    """
    Searched for a chapter by title, cuts out its text and assigns only those footnotes which IDs appear in the chapter content.

    Args:
        markdown_text(str): Full markdown text.
        headers(list[dict[str, str]]): List of headers returned by the MarkdownAnalyzer.
        all_footnotes(Footnotes): FootnoteSet with all footnotes from the text.
        chapter_title(str): Title of the chapter to be found.
        footnotes_start_line(Optional[int] = None): Line number where the footnote section begins.
    Returns:
        ChapterContent: Object representing the found chapter.
    """

    if not headers:
        return ChapterContent(text="", footnotes=None)
    
    chapter_heading = next((h for h in headers if chapter_title == h["text"]), None)

    if chapter_heading is None:
        return ChapterContent(text="", footnotes=None)
    
    start_line = chapter_heading["line"]
    subsequent = [h for h in headers if h["line"] > start_line and h["level"] <= chapter_heading["level"]]
    end_line = (subsequent[0]["line"] if subsequent else len(markdown_text.splitlines()) + 1)

    if footnotes_start_line is not None:
        end_line = min(end_line, footnotes_start_line)

    lines = markdown_text.splitlines()
    chapter_text = "\n".join(lines[start_line - 1 : end_line - 1])

    footnotes_ids = set(re.findall(r"\[\^([^\]]+)\]", chapter_text))
    chapter_footnotes = [f for f in all_footnotes.items if f.id in footnotes_ids]

    if chapter_footnotes:
        footnote_set = FootnoteSet(items=chapter_footnotes)
    else:
        footnote_set = None

    return ChapterContent(text=chapter_text, footnotes=footnote_set)

def extract_chapters(
        markdown_text: str,
        headers: list[dict[str, any]],
        footnotes_raw: list[dict[str, str]],
        book_id: str,
    ) -> list[Chapter]:
    """
    Divides the text into chapters and creates Chapter entities with ChapterContent including corresponding 
    footnotes (text + footnotes).

    Args:
        markdown_text(str): Full markdown text.
        headers(list[dict[str, str]]): List of headers returned by the MarkdownAnalyzer.
        footnotes_raw(Footnotes): A raw list of dictionaries from the MarkdownAnalyzer representing footnotes.
        book_id(str): The identifier of the book to which the chapters being created belong.

    Returns:
        list[Chapter]: List of Chapter entities representing the structure of headers (# and ##) along with their 
        content (ChapterContent) and footnotes (FootnoteSet assigned per chapter).
    """

    all_footnotes = _make_all_footnotes(footnotes_raw=footnotes_raw)

    footnotes_start_line = None
    if footnotes_raw:
        footnotes_start_line = min(f["line"] for f in footnotes_raw)

    headers_chapters = [
        (m.start(), m.group(2).strip(), 1)
        for m in re.finditer(r"^(#)\s+(.*)", markdown_text, re.MULTILINE)
    ]
    headers_subchapters = [
        (m.start(), m.group(2).strip(), 2)
        for m in re.finditer(r"^(##)\s+(.*)", markdown_text, re.MULTILINE)
    ]
    headers_sorted = sorted(headers_chapters + headers_subchapters, key=lambda x: x[0])

    chapters = []
    last_parent_id = None

    for i, (pos, title, level) in enumerate(headers_sorted):
        chapter_id = uuid.uuid4().hex[:6]

        content = _get_chapter_content_by_title(
            markdown_text=markdown_text,
            headers=headers,
            all_footnotes=all_footnotes,
            chapter_title=title,
            footnotes_start_line=footnotes_start_line,
        )

        if level == 1:
            parent_id = None
            last_parent_id = chapter_id
        else:
            parent_id = last_parent_id

        chapter = Chapter(
            id=chapter_id,
            book_id=book_id,
            chapter_number=i + 1,
            title=title,
            parent_id=parent_id,
            content=content,
        )
        chapters.append(chapter)

    return chapters