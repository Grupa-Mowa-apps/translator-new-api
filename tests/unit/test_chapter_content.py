import pytest
from app.domain.value_objects.chapter_content import ChapterContent
from app.domain.value_objects.footnotes import Footnote, FootnoteSet


def test_chapter_content_creation_without_footnotes():
    content = ChapterContent(text="Test content")
    assert content.text == "Test content"
    assert content.footnotes is None


def test_chapter_content_creation_with_footnotes():
    f1 = Footnote(id="1", text="First footnote")
    fs = FootnoteSet([f1])
    content = ChapterContent(text="Test content", footnotes=fs)
    assert content.text == "Test content"
    assert content.footnotes == fs


def test_chapter_content_footnote_count_without_footnotes():
    content = ChapterContent(text="Test")
    assert content.footnote_count == 0


def test_chapter_content_footnote_count_with_footnotes():
    f1 = Footnote(id="1", text="First")
    f2 = Footnote(id="2", text="Second")
    fs = FootnoteSet([f1, f2])
    content = ChapterContent(text="Test", footnotes=fs)
    assert content.footnote_count == 2


def test_chapter_content_str_without_footnotes():
    content = ChapterContent(text="Test content")
    result = str(content)
    assert "text_len=12" in result
    assert "footnotes_count=0" in result


def test_chapter_content_str_with_footnotes():
    f1 = Footnote(id="1", text="First")
    fs = FootnoteSet([f1])
    content = ChapterContent(text="Test", footnotes=fs)
    result = str(content)
    assert "text_len=4" in result
    assert "footnotes_count=1" in result


def test_chapter_content_repr():
    content = ChapterContent(text="Test")
    result = repr(content)
    assert "ChapterContent" in result
    assert "text='Test'" in result


def test_chapter_content_is_immutable():
    content = ChapterContent(text="Test")
    with pytest.raises(Exception):  # FrozenInstanceError
        content.text = "New text"
