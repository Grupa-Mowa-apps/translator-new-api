from app.infrastructure.db.models import UserDB, BookDB, ChapterDB

def seed_book_with_chapters(db):
    user = UserDB(id="u1", email="x@x.com")
    book = BookDB(id="b1", owner_id="u1", title="T", genre="g", quotation_marks="fr", status="uploaded", version=1)
    chapter1 = ChapterDB(id="c1", book_id="b1", content="p1")
    chapter2 = ChapterDB(id="c2", book_id="b1", parent_id="c1", content="p2")
    db.add_all([user, book, chapter1, chapter2])
    db.commit()

def test_deleting_book_removes_linked_chapters(db_session):
    seed_book_with_chapters(db_session)
    book = db_session.get(BookDB, "b1")
    db_session.delete(book)
    db_session.commit()

    assert db_session.get(ChapterDB, "c1") is None
    assert db_session.get(ChapterDB, "c2") is None