from app.infrastructure.db.models import UserDB, BookDB, ChapterDB

def test_user_book_chapter_crud(db_session):
    user = UserDB()
    user.id = "u1"
    user.email = "a@b.com"
    user.name = "Sara"
    db_session.add(user)

    book = BookDB()
    book.id = "b1"
    book.owner_id = "u1"
    book.title = "title"
    book.genre = "genre"
    book.quotation_marks = "fr"
    book.file_path = "/tmp/x.md"
    book.status = "uploaded"
    book.version = 1
    db_session.add(book)

    chapter1 = ChapterDB()
    chapter1.id = "c1"
    chapter1.book_id = "b1"
    chapter1.parent_id = None
    chapter1.content = "Chapter 1"
    
    chapter2 = ChapterDB()
    chapter2.id = "c2"
    chapter2.book_id = "b1"
    chapter2.parent_id = "c1"
    chapter2.content = "Subchapter 1.1"
    db_session.add_all([chapter1, chapter2])

    db_session.commit()
    db_session.expire_all()

    get_user = db_session.get(UserDB, "u1")
    assert len(get_user.books) == 1
    get_book = db_session.get(BookDB, "b1")
    assert len(get_book.chapters) == 2

    parent = db_session.get(ChapterDB, "c1")
    assert any(c.id == "c2" for c in parent.children)