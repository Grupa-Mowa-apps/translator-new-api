import pytest
from app.domain.entities.file import File
from app.domain.value_objects.file_kind import FileKind
from app.domain.errors import FileErrors

class TestFileEntity:
    def test_create_file_with_required_fields(self):
        file = File(
            id="file123",
            owner_id="owner123",
            kind=FileKind.MARKDOWN,
            path="file-path.md",
            filename="filename",
            book_id="book123",
        )

        assert file.id == "file123"
        assert file.owner_id == "owner123"
        assert file.kind == FileKind.MARKDOWN
        assert file.path == "file-path.md"
        assert file.filename == "filename"
        assert file.book_id == "book123"

    def test_rename_updates_filename_and_version(self):
        file = File(
            id="file123",
            owner_id="owner123",
            kind=FileKind.MARKDOWN,
            path="file-path.md",
            filename="filename",
            book_id="book123",
        )
        initial_version = file.version

        file.rename("newname")

        assert file.filename == "newname"
        assert file.version == initial_version + 1

    def test_rename_strips_whitespaces(self):
        file = File(
            id="file123",
            owner_id="owner123",
            kind=FileKind.MARKDOWN,
            path="file-path.md",
            filename="filename",
            book_id="book123",
        )

        file.rename("      newname        ")

        assert file.filename == "newname"

    def test_rename_with_empty_string_raises_error(self):
        file = File(
            id="file123",
            owner_id="owner123",
            kind=FileKind.MARKDOWN,
            path="file-path.md",
            filename="filename",
            book_id="book123",
        )

        with pytest.raises(ValueError) as e:
            file.rename("")
        assert str(e.value) == FileErrors.FILENAME_CANNOT_BE_EMPTY

    def test_rename_with_whitespaces_only_raises_error(self):
        file = File(
            id="file123",
            owner_id="owner123",
            kind=FileKind.MARKDOWN,
            path="file-path.md",
            filename="filename",
            book_id="book123",
        )

        with pytest.raises(ValueError) as e:
            file.rename("    ")
        assert str(e.value) == FileErrors.FILENAME_CANNOT_BE_EMPTY

    def test_move_to_updates_path_and_version(self):
        file = File(
            id="file123",
            owner_id="owner123",
            kind=FileKind.MARKDOWN,
            path="file-path.md",
            filename="filename",
            book_id="book123",
        )
        initial_version = file.version

        file.move_to("new-file-path.md")

        assert file.path == "new-file-path.md"
        assert file.version == initial_version + 1

    def test_move_to_strips_whitespaces_from_new_path_name(self):
        file = File(
            id="file123",
            owner_id="owner123",
            kind=FileKind.MARKDOWN,
            path="file-path.md",
            filename="filename",
            book_id="book123",
        )

        file.move_to("         new-file-path.md         ")

        assert file.path == "new-file-path.md"

    def test_move_to_empty_path_raises_error(self):
        file = File(
            id="file123",
            owner_id="owner123",
            kind=FileKind.MARKDOWN,
            path="file-path.md",
            filename="filename",
            book_id="book123",
        )

        with pytest.raises(ValueError) as e:
            file.move_to("")
        assert str(e.value) == FileErrors.PATH_CANNOT_BE_EMPTY

    def test_change_owner_updates_owner_and_version(self):
        file = File(
            id="file123",
            owner_id="owner123",
            kind=FileKind.MARKDOWN,
            path="file-path.md",
            filename="filename",
            book_id="book123",
        )
        initial_version = file.version

        file.change_owner("new-owner")

        assert file.owner_id == "new-owner"
        assert file.version == initial_version + 1

    def test_change_owner_strips_whitespaces_from_new_owner(self):
        file = File(
            id="file123",
            owner_id="owner123",
            kind=FileKind.MARKDOWN,
            path="file-path.md",
            filename="filename",
            book_id="book123",
        )

        file.change_owner("         new-owner        ")

        assert file.owner_id == "new-owner"

    def test_change_owner_with_empty_string_raises_error(self):
        file = File(
            id="file123",
            owner_id="owner123",
            kind=FileKind.MARKDOWN,
            path="file-path.md",
            filename="filename",
            book_id="book123",
        )

        with pytest.raises(ValueError) as e:
            file.change_owner("")
        assert str(e.value) == FileErrors.OWNER_ID_CANNOT_BE_EMPTY

    def test_attach_to_book_sets_book_id_and_updates_version(self):
        file = File(
            id="file123",
            owner_id="owner123",
            kind=FileKind.MARKDOWN,
            path="file-path.md",
            filename="filename",
        )
        initial_version = file.version

        file.attach_to_book("book-id")

        assert file.book_id == "book-id"
        assert file.version == initial_version + 1

    def test_attach_to_book_strips_whitespaces_from_book_id(self):
        file = File(
            id="file123",
            owner_id="owner123",
            kind=FileKind.MARKDOWN,
            path="file-path.md",
            filename="filename",
        )

        file.attach_to_book("        book-id        ")

        assert file.book_id == "book-id"

    def test_attach_to_book_with_empty_string_raises_error(self):
        file = File(
            id="file123",
            owner_id="owner123",
            kind=FileKind.MARKDOWN,
            path="file-path.md",
            filename="filename",
        )

        with pytest.raises(ValueError) as e:
            file.attach_to_book("")
        assert str(e.value) == FileErrors.BOOK_ID_CANNOT_BE_EMPTY

    def test_detach_from_book_removes_book_id_and_updates_version(self):
        file = File(
            id="file123",
            owner_id="owner123",
            kind=FileKind.MARKDOWN,
            path="file-path.md",
            filename="filename",
            book_id="book123",
        )
        initial_version = file.version

        file.detach_from_book()

        assert file.book_id == None
        assert file.version == initial_version + 1

    def test_detach_from_book_when_already_detached(self):
        file = File(
            id="file123",
            owner_id="owner123",
            kind=FileKind.MARKDOWN,
            path="file-path.md",
            filename="filename",
        )

        file.detach_from_book()
        
        assert file.book_id == None

    def test_change_kind_updates_kind_and_version(self):
        file = File(
            id="file123",
            owner_id="owner123",
            kind=FileKind.MARKDOWN,
            path="file-path.md",
            filename="filename",
            book_id="book123",
        )
        initial_version = file.version

        file.change_kind(FileKind.XLSX)

        assert file.kind == FileKind.XLSX
        assert file.version == initial_version + 1

    def test_change_kind_with_invalid_type_raises_error(self):
        file = File(
            id="file123",
            owner_id="owner123",
            kind=FileKind.MARKDOWN,
            path="file-path.md",
            filename="filename",
            book_id="book123",
        )

        with pytest.raises(ValueError) as e:
            file.change_kind("not-a-file-kind")
        assert str(e.value) == FileErrors.INVALID_FILE_KIND