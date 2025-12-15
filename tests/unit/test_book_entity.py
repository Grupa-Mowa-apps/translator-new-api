import pytest
from app.domain.entities.book import Book
from app.domain.entities.chapter import Chapter
from app.domain.value_objects.quotation_marks import QuoteType
from app.domain.value_objects.book_status import BookStatus

@pytest.fixture
def book():
    chapter = Chapter(id="c1", book_id="b1", chapter_number=1, title="Intro")
    return Book(
        id="b1",
        owner_id="u1",
        title="Title",
        genre="essay",
        quotation_marks=QuoteType.FR,
        file_path=None,
        chapters=[chapter],
    )

# CODE REVIEW: Uprość test - usuń niepotrzebne przypisania
# MAJOR: book = book jest redundantne (fixture już dostarcza book)
# SUGGESTION: Użyj initial_version i sprawdzaj przyrosty
def test_book_version_increments_on_changes(book):
    book = book  # TODO: Usuń to - niepotrzebne
    version = book.version
    book.rename_title("New Title")
    assert book.version == version + 1
    version = book.version  # TODO: Można uprościć - użyj initial_version + 2
    book.change_genre("science")
    assert book.version == version + 1
    version = book.version  # TODO: Można uprościć - użyj initial_version + 3
    book.change_quotation_marks(QuoteType.GR)
    assert book.version == version + 1

# CODE REVIEW: Usuń redundantne przypisanie
def test_invalid_title_raises_error(book):
    book = book  # TODO: Usuń - niepotrzebne
    with pytest.raises(ValueError):
        book.rename_title("  ")

# CODE REVIEW: Usuń redundantne przypisanie
def test_change_genre_validation(book):
    book = book  # TODO: Usuń - niepotrzebne
    with pytest.raises(ValueError):
        book.change_genre("")

# CODE REVIEW: Usuń redundantne przypisanie
def test_status_flow_happy_path(book):
    book = book  # TODO: Usuń - niepotrzebne
    assert book.status == BookStatus.UPLOADED

    book.mark_parsed()
    assert book.status == BookStatus.PARSED

    book.mark_ready_to_translate()
    assert book.status == BookStatus.READY_TO_TRANSLATE

    book.start_translation()
    assert book.status == BookStatus.IN_TRANSLATION

    book.mark_translated()
    assert book.status == BookStatus.TRANSLATED

# CODE REVIEW: Usuń redundantne przypisanie i rozdziel asserty
# NIT: Złożony assert - lepiej rozdzielić na dwa
def test_mark_failed_sets_failed_and_bumps_version(book):
    book = book  # TODO: Usuń - niepotrzebne
    version = book.version
    book.mark_failed()
    # TODO: Rozdziel na dwa asserty dla lepszej czytelności:
    # assert book.status == BookStatus.FAILED
    # assert book.version == version + 1
    assert book.status == BookStatus.FAILED and book.version == version + 1
