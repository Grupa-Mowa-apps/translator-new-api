import pytest
from app.domain.entities.chapter import Chapter

def test_chapter_becomes_subchapter_when_parent_set():
    chapter = Chapter(id="c1", book_id="b1", chapter_number=1, title="Intro")
    assert chapter.is_subchapter() is False
    chapter.set_parent("p1")
    assert chapter.is_subchapter() is True

def test_rename_title_strips_and_updates():
    ch = Chapter(id="c1", book_id="b1", chapter_number=1, title="Pink")
    ch.rename_title("  Blue  ")
    assert ch.title == "Blue"

def test_rename_title_validation():
    ch = Chapter(id="c1", book_id="b1", chapter_number=1, title="Intro")
    with pytest.raises(ValueError):
        ch.rename_title("     ")

def test_cannot_set_self_as_parent():
    ch = Chapter(id="c1", book_id="b1", chapter_number=1, title="Intro")
    with pytest.raises(ValueError):
        ch.set_parent("c1")