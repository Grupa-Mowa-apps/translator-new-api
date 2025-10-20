from app.infrastructure.db.models import UserDB, BookDB, ChapterDB

def test_user_book_chapter_crud(db_session):
    user = UserDB(id="u1", email="a@b.com", name="Sara")
    db_session.add(user)

    book = BookDB(
        id="b1", owner_id="u1",
        title="title", genre="genre", quotation_marks="fr",
        file_path="/tmp/x.md", status="uploaded", version=1
    )
    db_session.add(book)

    chapter1 = ChapterDB(id="c1", book_id="b1", parent_id=None, content="Chapter 1")
    chapter2 = ChapterDB(id="c2", book_id="b1", parent_id="c1", content="Subchapter 1.1")
    db_session.add_all([chapter1, chapter2])

    db_session.commit()
    db_session.expire_all()

    get_user = db_session.get(UserDB, "u1")
    assert len(get_user.books) == 1
    get_book = db_session.get(BookDB, "b1")
    assert len(get_book.chapters) == 2

    parent = db_session.get(ChapterDB, "c1")
    assert any(c.id == "c2" for c in parent.children)