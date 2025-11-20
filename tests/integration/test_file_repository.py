import pytest
from sqlalchemy.orm.session import Session

from app.infrastructure.db.models import BookDB, FileDB, UserDB
from app.infrastructure.db.repositories.file_repo_sqlalchemy import SqlAlchemyFileRepository
from app.domain.entities.file import File
from app.domain.value_objects.file_kind import FileKind
from app.domain.value_objects.quotation_marks import QuoteType
from app.domain.errors import FileErrors

@pytest.fixture
def file_repository(db_session: Session):
    return SqlAlchemyFileRepository(db_session)

@pytest.fixture
def owners(db_session: Session):
    users = [
        UserDB(id="owner1", email="owner1@example.com", name="Owner One"),
        UserDB(id="owner2", email="owner2@example.com", name="Owner Two"),
        UserDB(id="owner4", email="owner4@example.com", name="Owner Four"),
        UserDB(id="owner5", email="owner5@example.com", name="Owner Five"),
    ]
    db_session.add_all(users)
    db_session.flush()
    return users

@pytest.fixture
def books(db_session: Session, owners):
    books = [
        BookDB(id="book1", owner_id="owner1", title="Book One", genre="genre1", quotation_marks=QuoteType.FR),
        BookDB(id="book2",owner_id="owner2", title="Book Two", genre="genre2", quotation_marks=QuoteType.FR),
    ]
    db_session.add_all(books)
    db_session.flush()
    return books

class TestSqlAlchemyFileRepository:
    def test_add_and_get_file(self, file_repository, db_session, owners):
        file = File(
            id="file1", owner_id="owner1", 
            kind=FileKind.MARKDOWN, path="file.md", filename="markdown-file",
        )

        file_repository.add(file)
        db_session.flush()

        retrieved_file = file_repository.get("file1")
        
        assert retrieved_file is not None
        assert retrieved_file.id == "file1"
        assert retrieved_file.owner_id == "owner1"
        assert retrieved_file.kind == FileKind.MARKDOWN
        assert retrieved_file.path == "file.md"
        assert retrieved_file.filename == "markdown-file"
        assert retrieved_file.book_id is None
        assert retrieved_file.version == 1

    def test_add_file_with_book_id(self, file_repository, db_session, owners, books):
        file = File(
            id="file2", owner_id="owner1", 
            kind=FileKind.MARKDOWN, path="file.md", filename="markdown-file",
            book_id="book1"
        )

        file_repository.add(file)
        db_session.flush()

        retrieved_file = file_repository.get("file2")

        assert retrieved_file is not None
        assert retrieved_file.id == "file2"
        assert retrieved_file.owner_id == "owner1"
        assert retrieved_file.kind == FileKind.MARKDOWN
        assert retrieved_file.path == "file.md"
        assert retrieved_file.filename == "markdown-file"
        assert retrieved_file.book_id == "book1"
        assert retrieved_file.version == 1

    def test_get_nonexistant_file_raises_error(slef, file_repository, db_session):
        with pytest.raises(ValueError) as e:
            file_repository.get("nonexistant-id")
        assert str(e.value) == FileErrors.FILE_NOT_FOUND

    def test_update_file(self, file_repository, db_session, owners):
        file = File(
            id="file1", owner_id="owner1", 
            kind=FileKind.MARKDOWN, path="file.md", filename="markdown-file",
        )
        file_repository.add(file)
        db_session.flush()

        file.kind = FileKind.TRANSALTED_MARKDOWN
        file.path = "translated-file.xlsx"
        file.filename = "translated-markdown-file"
        
        file_repository.update(file)
        db_session.flush()

        updated_file = file_repository.get("file1")

        assert updated_file is not None
        assert updated_file.id == "file1"
        assert updated_file.owner_id == "owner1"
        assert updated_file.kind == FileKind.TRANSALTED_MARKDOWN
        assert updated_file.path == "translated-file.xlsx"
        assert updated_file.filename == "translated-markdown-file"
        assert updated_file.book_id is None

    def test_update_file_add_book_id(self, file_repository, db_session, owners, books):
        file = File(
            id="file2", owner_id="owner1", 
            kind=FileKind.MARKDOWN, path="file.md", filename="markdown-file",
        )
        file_repository.add(file)
        db_session.flush()

        file.kind = FileKind.TRANSALTED_MARKDOWN
        file.path = "translated-file.xlsx"
        file.filename = "translated-markdown-file"
        file.book_id = "book1"

        file_repository.update(file)
        db_session.flush()

        updated_file = file_repository.get("file2")

        assert updated_file is not None
        assert updated_file.id == "file2"
        assert updated_file.owner_id == "owner1"
        assert updated_file.kind == FileKind.TRANSALTED_MARKDOWN
        assert updated_file.path == "translated-file.xlsx"
        assert updated_file.filename == "translated-markdown-file"
        assert updated_file.book_id == "book1"

    def test_update_nonexistant_file_raises_error(self, file_repository, db_session):
        file = File(
            id="file1", owner_id="owner1", 
            kind=FileKind.MARKDOWN, path="file.md", filename="markdown-file",
        )

        with pytest.raises(ValueError) as e:
            file_repository.update(file)
        assert str(e.value) == FileErrors.FILE_NOT_FOUND

    def test_delete_file(self, file_repository, db_session, owners):
        file = File(
            id="file1", owner_id="owner1", 
            kind=FileKind.MARKDOWN, path="file.md", filename="markdown-file",
        )
        file_repository.add(file)
        db_session.flush()

        file_repository.delete("file1")

        with pytest.raises(ValueError) as e:
            file_repository.get("file1")
        assert str(e.value) == FileErrors.FILE_NOT_FOUND

    def test_delete_nonexistant_file_raises_error(self, file_repository, db_session):
        with pytest.raises(ValueError) as e:
            file_repository.delete("nonexistant-id")
        assert str(e.value) == FileErrors.FILE_NOT_FOUND

    def test_list_files_for_owner_no_filter(self, file_repository, db_session, owners):
        files = [
            File(id="file1", owner_id="owner1", kind=FileKind.MARKDOWN, path="file1.md", filename="markdown-file1"),
            File(id="file2", owner_id="owner2", kind=FileKind.XLSX, path="file2.xlsx", filename="excel-file2"),
            File(id="file3", owner_id="owner1", kind=FileKind.TRANSALTED_MARKDOWN, path="file3.md", filename="markdown-file3"),
            File(id="file4", owner_id="owner4", kind=FileKind.MARKDOWN, path="file4.md", filename="markdown-file4"),
            File(id="file5", owner_id="owner5", kind=FileKind.MARKDOWN, path="file5.md", filename="markdown-file5"),
            File(id="file6", owner_id="owner1", kind=FileKind.TRANSALTED_MARKDOWN, path="file6.md", filename="markdown-file6"),
        ]
        for file in files:
            file_repository.add(file)
            db_session.flush()

        result = file_repository.list_files_for_owner(owner_id="owner1", kind=None, limit=2)

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0].owner_id == "owner1"
        assert result[0].owner_id == result[1].owner_id
        assert result[1].id == "file3"

    def test_list_files_for_owner_with_filter(self, file_repository, db_session, owners):
        files = [
            File(id="file1", owner_id="owner1", kind=FileKind.MARKDOWN, path="file1.md", filename="markdown-file1"),
            File(id="file2", owner_id="owner2", kind=FileKind.XLSX, path="file2.xlsx", filename="excel-file2"),
            File(id="file3", owner_id="owner1", kind=FileKind.TRANSALTED_MARKDOWN, path="file3.md", filename="markdown-file3"),
            File(id="file4", owner_id="owner4", kind=FileKind.MARKDOWN, path="file4.md", filename="markdown-file4"),
            File(id="file5", owner_id="owner5", kind=FileKind.MARKDOWN, path="file5.md", filename="markdown-file5"),
            File(id="file6", owner_id="owner1", kind=FileKind.TRANSALTED_MARKDOWN, path="file6.md", filename="markdown-file6"),
            File(id="file7", owner_id="owner1", kind=FileKind.TRANSALTED_MARKDOWN, path="file7.xlsx", filename="markdown-file7"),
        ]
        for file in files:
            file_repository.add(file)
            db_session.flush()

        result = file_repository.list_files_for_owner(owner_id="owner1", kind=FileKind.TRANSALTED_MARKDOWN, limit=2)

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0].owner_id == "owner1"
        assert result[0].owner_id == result[1].owner_id
        assert result[1].kind == FileKind.TRANSALTED_MARKDOWN
        assert result[0].kind == result[1].kind
        assert result[0].id == "file3"
        assert result[1].id == "file6"

    def test_list_files_for_book_no_filter(self, file_repository, db_session, owners, books):
        files = [
            File(id="file1", owner_id="owner1", kind=FileKind.MARKDOWN, path="file1.md", filename="markdown-file1", book_id="book1"),
            File(id="file2", owner_id="owner2", kind=FileKind.XLSX, path="file2.xlsx", filename="excel-file2", book_id="book1"),
            File(id="file3", owner_id="owner1", kind=FileKind.TRANSALTED_MARKDOWN, path="file3.md", filename="markdown-file3", book_id="book2"),
            File(id="file4", owner_id="owner4", kind=FileKind.MARKDOWN, path="file4.md", filename="markdown-file4", book_id="book1"),
            File(id="file5", owner_id="owner5", kind=FileKind.MARKDOWN, path="file5.md", filename="markdown-file5", book_id="book1"),
            File(id="file6", owner_id="owner1", kind=FileKind.TRANSALTED_MARKDOWN, path="file6.md", filename="markdown-file6", book_id="book1"),
        ]
        for file in files:
            file_repository.add(file)
            db_session.flush()

        result = file_repository.list_files_for_book(book_id="book1", kind=None, limit=3)

        assert isinstance(result, list)
        assert len(result) == 3
        assert result[2].owner_id == "owner4"
        assert result[0].id == "file2"
        assert result[1].path == "file1.md"
        assert result[0].book_id == result[1].book_id == result[2].book_id == "book1"

    def test_list_files_for_book_with_filter(self, file_repository, db_session, owners, books):
        files = [
            File(id="file1", owner_id="owner1", kind=FileKind.MARKDOWN, path="file1.md", filename="markdown-file1", book_id="book1"),
            File(id="file2", owner_id="owner2", kind=FileKind.XLSX, path="file2.xlsx", filename="excel-file2", book_id="book1"),
            File(id="file3", owner_id="owner1", kind=FileKind.TRANSALTED_MARKDOWN, path="file3.md", filename="markdown-file3", book_id="book2"),
            File(id="file4", owner_id="owner4", kind=FileKind.MARKDOWN, path="file4.md", filename="markdown-file4", book_id="book1"),
            File(id="file5", owner_id="owner5", kind=FileKind.MARKDOWN, path="file5.md", filename="markdown-file5", book_id="book1"),
            File(id="file6", owner_id="owner1", kind=FileKind.TRANSALTED_MARKDOWN, path="file6.md", filename="markdown-file6", book_id="book1"),
        ]
        for file in files:
            file_repository.add(file)
            db_session.flush()

        result = file_repository.list_files_for_book(book_id="book1", kind=FileKind.MARKDOWN, limit=2)

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0].id == "file1"
        assert result[1].path == "file4.md"
        assert result[0].book_id == result[1].book_id == "book1"
        assert result[0].kind == result[1].kind == FileKind.MARKDOWN