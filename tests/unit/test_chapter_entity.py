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

def test_chapter_number_must_be_positive():
    with pytest.raises(ValueError, match="Chapter number must be greater than 0"):
        Chapter(id="c1", book_id="b1", chapter_number=0, title="Intro")
    
    with pytest.raises(ValueError, match="Chapter number must be greater than 0"):
        Chapter(id="c2", book_id="b1", chapter_number=-1, title="Intro")

def test_set_parent_to_none_clears_parent():
    ch = Chapter(id="c1", book_id="b1", chapter_number=1, title="Intro")
    ch.set_parent("p1")
    assert ch.is_subchapter() is True
    
    ch.set_parent(None)
    assert ch.is_subchapter() is False
    assert ch.parent_id is None