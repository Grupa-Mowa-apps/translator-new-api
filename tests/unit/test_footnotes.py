import pytest
from app.domain.value_objects.footnotes import Footnote, FootnoteSet


def test_footnote_creation():
    footnote = Footnote(id="1", text="Test footnote")
    assert footnote.id == "1"
    assert footnote.text == "Test footnote"


def test_footnote_strips_whitespace():
    footnote = Footnote(id="  1  ", text="  Test  ")
    assert footnote.id == "1"
    assert footnote.text == "Test"


def test_footnote_empty_id_raises():
    with pytest.raises(ValueError, match="Footnote id cannot be empty"):
        Footnote(id="", text="Test")


def test_footnote_whitespace_only_id_raises():
    with pytest.raises(ValueError, match="Footnote id cannot be empty"):
        Footnote(id="   ", text="Test")


def test_footnote_empty_text_raises():
    with pytest.raises(ValueError, match="Footnote text cannot be empty"):
        Footnote(id="1", text="")


def test_footnote_whitespace_only_text_raises():
    with pytest.raises(ValueError, match="Footnote text cannot be empty"):
        Footnote(id="1", text="   ")


def test_footnote_str():
    footnote = Footnote(id="1", text="Test footnote")
    assert str(footnote) == "[^1]: Test footnote"


def test_footnote_repr():
    footnote = Footnote(id="1", text="Test")
    assert "Footnote" in repr(footnote)
    assert "id='1'" in repr(footnote)
    assert "text='Test'" in repr(footnote)


def test_footnote_is_immutable():
    footnote = Footnote(id="1", text="Test")
    with pytest.raises(Exception):  # FrozenInstanceError
        footnote.id = "2"


def test_footnote_set_creation():
    f1 = Footnote(id="1", text="First")
    f2 = Footnote(id="2", text="Second")
    fs = FootnoteSet([f1, f2])
    assert len(fs) == 2
    assert fs.items == [f1, f2]


def test_footnote_set_empty():
    fs = FootnoteSet([])
    assert len(fs) == 0


def test_footnote_set_len():
    f1 = Footnote(id="1", text="First")
    f2 = Footnote(id="2", text="Second")
    f3 = Footnote(id="3", text="Third")
    fs = FootnoteSet([f1, f2, f3])
    assert len(fs) == 3


def test_footnote_set_duplicate_ids_raises():
    f1 = Footnote(id="1", text="First")
    f2 = Footnote(id="1", text="Duplicate")
    with pytest.raises(ValueError, match="Duplicate footnote ids found"):
        FootnoteSet([f1, f2])


def test_footnote_set_str():
    f1 = Footnote(id="1", text="First")
    f2 = Footnote(id="2", text="Second")
    fs = FootnoteSet([f1, f2])
    result = str(fs)
    assert "Footnotes(2)" in result
    assert "[^1]: First" in result
    assert "[^2]: Second" in result


def test_footnote_set_str_empty():
    fs = FootnoteSet([])
    assert str(fs) == "Footnotes(0):"


def test_footnote_set_repr():
    f1 = Footnote(id="1", text="First")
    fs = FootnoteSet([f1])
    result = repr(fs)
    assert "FootnoteSet" in result
    assert "count=1" in result


def test_footnote_set_is_immutable():
    f1 = Footnote(id="1", text="First")
    fs = FootnoteSet([f1])
    with pytest.raises(Exception):  # FrozenInstanceError
        fs.items = []
