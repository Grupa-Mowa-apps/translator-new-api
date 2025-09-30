import pytest
from app.domain.entities.book import Book
from app.domain.entities.chapter import Chapter
from app.domain.value_objects.quotation_marks import QuoteType
from app.domain.value_objects.book_status import BookStatus

def _book():
    ch = Chapter(id="c1", book_id="b1", chapter_number=1, title="Intro")
    return Book(
        id="b1",
        owner_id="u1",
        title="Title",
        genre="essay",
        quotation_marks=QuoteType.FR,
        file_path=None,
        chapters=[ch],
    )

def test_version_bumps_on_mutations():
    b = _book()
    v = b.version
    b.rename_title("New Title")
    assert b.version == v + 1
    v = b.version
    b.change_genre("science")
    assert b.version == v + 1
    v = b.version
    b.change_quotation_marks(QuoteType.GE)
    assert b.version == v + 1

def test_rename_title_validation():
    b = _book()
    with pytest.raises(ValueError):
        b.rename_title("  ")

def test_change_genre_validation():
    b = _book()
    with pytest.raises(ValueError):
        b.change_genre("")

def test_status_flow_happy_path():
    b = _book()
    assert b.status == BookStatus.UPLOADED
    b.mark_parsed();                 assert b.status == BookStatus.PARSED
    b.mark_ready_to_translate();     assert b.status == BookStatus.READY_TO_TRANSLATE
    b.start_translation();           assert b.status == BookStatus.IN_TRANSLATION
    b.mark_translated();             assert b.status == BookStatus.TRANSLATED

def test_mark_failed_sets_failed_and_bumps_version():
    b = _book()
    v = b.version
    b.mark_failed()
    assert b.status == BookStatus.FAILED and b.version == v + 1
