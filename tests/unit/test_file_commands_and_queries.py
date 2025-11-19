from typing import List
import pytest
from unittest.mock import Mock

from app.domain.entities.file import File
from app.domain.ports.file_repository import FileRepository
from app.application.commands.upload_file import UploadFileCommand
from app.application.commands.update_file import UpdateFileCommand
from app.application.commands.delete_file import DeleteFileCommand
from app.application.queries.get_file import GetFileQuery
from app.application.queries.list_files import ListFilesForOwnerQuery, ListFilesForBookQuery
from app.application.dto.file_dto import FileResponse, UploadFileRequest, UpdateFileRequest
from app.domain.value_objects.file_kind import FileKind
from app.domain.errors import FileErrors

@pytest.fixture
def mock_file_repository():
    return Mock(spec=FileRepository)

class TestFileCommands:
    def test_create_file_successfully(self, mock_file_repository):
        command = UploadFileCommand(mock_file_repository)
        dto = UploadFileRequest(
            owner_id="ownerid",
            kind=FileKind.MARKDOWN,
            filename="filename",
        )

        result = command.run(dto)

        mock_file_repository.add.assert_called_once()

        added_file = mock_file_repository.add.call_args[0][0]
        assert isinstance(added_file, File)
        assert added_file.owner_id == "ownerid"
        assert added_file.kind == FileKind.MARKDOWN
        assert added_file.filename == "filename"

        assert isinstance(result, FileResponse)
        assert result.id == added_file.id
        assert result.owner_id == added_file.owner_id
        assert result.kind == added_file.kind
        assert result.filename == added_file.filename

    def test_update_file(self, mock_file_repository):
        existing_file = File(
            id="file1", owner_id="owner1", 
            kind=FileKind.MARKDOWN, path="file.md", filename="markdown-file",
        )
        mock_file_repository.get.return_value = existing_file

        command = UpdateFileCommand(mock_file_repository)
        dto = UpdateFileRequest(
            owner_id="new-owner-id",
            kind=FileKind.XLSX,
            filename="new-filename"
        )

        result = command.run(file_id=existing_file.id, dto=dto)

        mock_file_repository.get.assert_called_once_with("file1")
        mock_file_repository.update.assert_called_once()

        assert result is not None
        assert isinstance(result, FileResponse)
        assert result.owner_id == "new-owner-id"
        assert result.kind == FileKind.XLSX
        assert result.filename == "new-filename"

    def test_delete_file_successfully(self, mock_file_repository):
        existing_file = File(
            id="file1", owner_id="owner1", 
            kind=FileKind.MARKDOWN, path="file.md", filename="markdown-file",
        )
        mock_file_repository.get.return_value = existing_file

        command = DeleteFileCommand(mock_file_repository)
        command.run(file_id="file1")

        mock_file_repository.get.assert_called_once_with("file1")
        mock_file_repository.delete.assert_called_once_with("file1")

    def test_should_reject_delete_nonexistent_file(self, mock_file_repository):
        mock_file_repository.get.return_value = None

        command = DeleteFileCommand(mock_file_repository)
        nonexistent_id = "nonexistent-id"

        with pytest.raises(ValueError) as e:
            command.run(nonexistent_id)
        assert str(e.value) == FileErrors.FILE_NOT_FOUND

class TestFileQueries:
    def test_get_file(self, mock_file_repository):
        file = File(
            id="file1", owner_id="owner1", 
            kind=FileKind.MARKDOWN, path="file.md", filename="markdown-file",
        )
        mock_file_repository.get.return_value = file

        query = GetFileQuery(mock_file_repository)
        file_id = "file1"

        result = query.run(file_id)

        mock_file_repository.get.assert_called_once_with("file1")

        assert result is not None
        assert isinstance(result, FileResponse)
        assert result.id == file.id
        assert result.owner_id == file.owner_id
        assert result.kind == file.kind
        assert result.path == file.path
        assert result.filename == file.filename

    def test_should_reject_get_nonexistent_file(self, mock_file_repository):
        mock_file_repository.get.return_value = None
        
        query = GetFileQuery(mock_file_repository)
        nonexistent_id = "345"

        with pytest.raises(ValueError) as e:
            result = query.run(nonexistent_id)
        assert str(e.value) == FileErrors.FILE_NOT_FOUND

    def test_list_files_for_owner(self, mock_file_repository):
        files = [
            File(id="file1", owner_id="owner1", kind=FileKind.MARKDOWN, path="file1.md", filename="markdown-file1"),
            File(id="file2", owner_id="owner2", kind=FileKind.XLSX, path="file2.xlsx", filename="excel-file2"),
            File(id="file3", owner_id="owner1", kind=FileKind.TRANSALTED_MARKDOWN, path="file3.md", filename="markdown-file3"),
            File(id="file4", owner_id="owner4", kind=FileKind.MARKDOWN, path="file4.md", filename="markdown-file4"),
            File(id="file5", owner_id="owner5", kind=FileKind.MARKDOWN, path="file5.md", filename="markdown-file5"),
        ]

        def side_effect(owner_id, kind, limit):
            owner_files = [f for f in files if f.owner_id == owner_id]
            return owner_files[:limit]

        mock_file_repository.list_files_for_owner.side_effect = side_effect

        query = ListFilesForOwnerQuery(mock_file_repository)
        result = query.run(owner_id="owner1", kind=None, limit=2)

        mock_file_repository.list_files_for_owner.assert_called_once_with("owner1", None, 2)

        assert result is not None
        assert isinstance(result, List)
        assert len(result) == 2
        assert result[0].id == "file1"
        assert result[0].owner_id == "owner1"
        assert result[0].owner_id == result[1].owner_id
        assert result[0].kind == FileKind.MARKDOWN

    def test_list_files_for_owner_with_filter(self, mock_file_repository):
        files = [
            File(id="file1", owner_id="owner1", kind=FileKind.MARKDOWN, path="file1.md", filename="markdown-file1"),
            File(id="file2", owner_id="owner2", kind=FileKind.XLSX, path="file2.xlsx", filename="excel-file2"),
            File(id="file3", owner_id="owner1", kind=FileKind.XLSX, path="file3.md", filename="excel-file3"),
            File(id="file4", owner_id="owner3", kind=FileKind.MARKDOWN, path="file4.md", filename="markdown-file4"),
            File(id="file5", owner_id="owner1", kind=FileKind.MARKDOWN, path="file5.md", filename="markdown-file5"),
        ]

        def side_effect(owner_id, kind, limit):
            owner_files = [f for f in files if f.owner_id == owner_id]

            if kind is not None:
                owner_files = [f for f in owner_files if f.kind == kind]
            
            return owner_files[:limit]

        mock_file_repository.list_files_for_owner.side_effect = side_effect

        query = ListFilesForOwnerQuery(mock_file_repository)
        result = query.run(owner_id="owner1", kind=FileKind.MARKDOWN, limit=2)

        mock_file_repository.list_files_for_owner.assert_called_once_with("owner1", FileKind.MARKDOWN, 2)

        assert result is not None
        assert isinstance(result, List)
        assert len(result) == 2
        assert result[0].id == "file1"
        assert result[1].id == "file5"

    def test_list_files_for_book(self, mock_file_repository):
        files = [
            File(id="file1", owner_id="owner1", kind=FileKind.MARKDOWN, path="file1.md", filename="markdown-file1", book_id="book1"),
            File(id="file2", owner_id="owner2", kind=FileKind.XLSX, path="file2.xlsx", filename="excel-file2", book_id="book2"),
            File(id="file3", owner_id="owner1", kind=FileKind.TRANSALTED_MARKDOWN, path="file3.md", filename="markdown-file3", book_id="book3"),
            File(id="file4", owner_id="owner4", kind=FileKind.MARKDOWN, path="file4.md", filename="markdown-file4", book_id="book2"),
            File(id="file5", owner_id="owner5", kind=FileKind.MARKDOWN, path="file5.md", filename="markdown-file5", book_id="book2"),
        ]

        def side_effect(book_id, kind, limit):
            book_files = [f for f in files if f.book_id == book_id]
            return book_files[:limit] if limit is not None else book_files

        mock_file_repository.list_files_for_book.side_effect = side_effect

        query = ListFilesForBookQuery(mock_file_repository)
        result = query.run(book_id="book2", kind=None, limit=None)

        mock_file_repository.list_files_for_book.assert_called_once_with("book2", None, None)

        assert result is not None
        assert isinstance(result, List)
        assert len(result) == 3
        assert result[0].id == "file2"
        assert result[1].owner_id == "owner4"
        assert result[0].book_id == result[1].book_id == result[2].book_id

    def test_list_files_for_book_with_filter(self, mock_file_repository):
        files = [
            File(id="file1", owner_id="owner1", kind=FileKind.MARKDOWN, path="file1.md", filename="markdown-file1", book_id="book1"),
            File(id="file2", owner_id="owner2", kind=FileKind.XLSX, path="file2.xlsx", filename="excel-file2", book_id="book2"),
            File(id="file3", owner_id="owner1", kind=FileKind.TRANSALTED_MARKDOWN, path="file3.md", filename="markdown-file3", book_id="book3"),
            File(id="file4", owner_id="owner4", kind=FileKind.MARKDOWN, path="file4.md", filename="markdown-file4", book_id="book2"),
            File(id="file5", owner_id="owner5", kind=FileKind.MARKDOWN, path="file5.md", filename="markdown-file5", book_id="book2"),
            File(id="file6", owner_id="owner6", kind=FileKind.MARKDOWN, path="file6.md", filename="markdown-file6", book_id="book2"),
        ]

        def side_effect(book_id, kind, limit):
            book_files = [f for f in files if f.book_id == book_id]

            if kind is not None:
                book_files = [f for f in book_files if f.kind == kind]

            return book_files[:limit] if limit is not None else book_files

        mock_file_repository.list_files_for_book.side_effect = side_effect

        query = ListFilesForBookQuery(mock_file_repository)
        result = query.run(book_id="book2", kind=FileKind.MARKDOWN, limit=2)

        mock_file_repository.list_files_for_book.assert_called_once_with("book2", FileKind.MARKDOWN, 2)

        assert result is not None
        assert isinstance(result, List)
        assert len(result) == 2
        assert isinstance(result[0], FileResponse)
        assert result[0].id == "file4"
        assert result[1].owner_id == "owner5"
        assert result[0].kind == result[1].kind