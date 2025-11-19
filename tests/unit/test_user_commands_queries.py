from typing import List
import pytest
from unittest.mock import Mock

from app.application.commands.create_user import CreateUserCommand
from app.application.commands.delete_user import DeleteUserCommand
from app.application.commands.update_user import UpdateUserCommand
from app.application.queries.get_user import GetUserQuery
from app.application.queries.list_users import ListUsersQuery
from app.application.queries.get_user_books import GetUserBooksCommand
from app.application.dto.user_dto import CreateUserRequest, UserResponse, UpdateUserRequest
from app.domain.entities.user import User
from app.domain.entities.book import Book
from app.domain.entities.book import Chapter
from app.domain.ports.book_repository import BookRepository
from app.domain.ports.user_repository import UserRepository
from app.domain.errors import UserErrors

@pytest.fixture
def mock_user_repository():
    return Mock(spec=UserRepository)

@pytest.fixture
def mock_book_repository():
    return Mock(spec=BookRepository)

class TestUserCommands:
    def test_create_user_successfully(self, mock_user_repository):
        mock_user_repository.get_by_email.return_value = None

        command = CreateUserCommand(mock_user_repository)
        dto = CreateUserRequest(email="test@example.com", name="test user")

        result = command.run(dto)
        mock_user_repository.get_by_email.assert_called_once_with("test@example.com")
        mock_user_repository.add.assert_called_once()

        added_user = mock_user_repository.add.call_args[0][0]
        assert isinstance(added_user, User)
        assert added_user.email == "test@example.com"
        assert added_user.name == "test user"
        assert added_user.id is not None

        assert isinstance(result, UserResponse)
        assert result.email == "test@example.com"
        assert result.name == "test user"
        assert result.id is not None

    def test_should_reject_duplicate_email(self, mock_user_repository):
        existing_user = User(id="existing123", email="existing@example.com", name="existing user")
        mock_user_repository.get_by_email.return_value = existing_user

        command = CreateUserCommand(mock_user_repository)
        dto = CreateUserRequest(email="existing@example.com", name="existing user")

        with pytest.raises(ValueError) as e:
            command.run(dto)
        assert str(e.value) == UserErrors.EMAIL_ALREADY_IN_USE

        mock_user_repository.add.assert_not_called()

    def test_should_generate_unique_id(self, mock_user_repository):
        mock_user_repository.get_by_email.return_value = None

        command = CreateUserCommand(mock_user_repository)
        dto1 = CreateUserRequest(email="test1@example.com", name="test user 1")
        dto2 = CreateUserRequest(email="test2@example.com", name="test user 2")

        result_user1 = command.run(dto1)
        result_user2 = command.run(dto2)

        assert result_user1.id is not None
        assert result_user2.id is not None
        assert result_user1.id != result_user2.id

    def test_delete_user_successfully(self, mock_user_repository):
        existing_user = User(id="existing123", email="existing@example.com", name="existing user")
        mock_user_repository.get_by_email.return_value = existing_user

        command = DeleteUserCommand(mock_user_repository)
        existing_id = "existing123"

        command.run(existing_id)
        
        mock_user_repository.get.assert_called_once_with(existing_id)
        mock_user_repository.delete.assert_called_once_with(existing_id)

    def test_should_reject_delete_nonexistent_user(self, mock_user_repository):
        mock_user_repository.get.return_value = None

        command = DeleteUserCommand(mock_user_repository)
        nonexistent_id = "nonexistent123"

        with pytest.raises(ValueError) as e:
            command.run(nonexistent_id)
        assert str(e.value) == UserErrors.USER_NOT_FOUND

        mock_user_repository.delete.assert_not_called()

    def test_update_user(self, mock_user_repository):
        existing_user = User(id="existing123", email="existing@example.com", name="existing user")
        mock_user_repository.get.return_value = existing_user

        command = UpdateUserCommand(mock_user_repository)
        dto = UpdateUserRequest(email="new-existing@example.com", name="new name")

        result = command.run(user_id="existing123", dto=dto)

        mock_user_repository.get.assert_called_once_with("existing123")
        mock_user_repository.update.assert_called_once()

        assert result is not None
        assert isinstance(result, UserResponse)
        assert result.email == "new-existing@example.com"
        assert result.name == "new name"

class TestUserQueries:
    def test_get_user(self, mock_user_repository):
        user = User(id="123", email="user@example.com", name="user")
        mock_user_repository.get.return_value = user
        
        query = GetUserQuery(mock_user_repository)
        user_id = "123"

        result = query.run(user_id)

        mock_user_repository.get.assert_called_once_with("123")

        assert isinstance(result, UserResponse)
        assert result.id == "123"
        assert result.email == "user@example.com"
        assert result.name == "user"

    def test_should_reject_get_nonexistent_user(self, mock_user_repository):
        mock_user_repository.get.return_value = None
        
        query = GetUserQuery(mock_user_repository)
        nonexistent_id = "345"

        with pytest.raises(ValueError) as e:
            result = query.run(nonexistent_id)
        assert str(e.value) == UserErrors.USER_NOT_FOUND

    def test_list_users(self, mock_user_repository):
        users = [
            User(id="user1", email="user1@email.com", name="user one"),
            User(id="user2", email="user2@email.com", name="user two"),
            User(id="user3", email="user3@email.com", name="user three"),
            User(id="user4", email="user4@email.com", name="user four"),
            User(id="user5", email="user5@email.com", name="user five")
        ]
        mock_user_repository.list_paginated_filtered.side_effect = (
            lambda limit, email_like: users[:limit]
        )

        query = ListUsersQuery(mock_user_repository)
        result = query.run(3, email_like=None)

        mock_user_repository.list_paginated_filtered.assert_called_once_with(3, None)

        assert isinstance(result, List)
        assert result[0].id == "user1"
        assert result[0].email == "user1@email.com"
        assert result[0].name == "user one"
        assert len(result) == 3

    def test_get_user_books(self, mock_user_repository, mock_book_repository):
        user = User(id="user", email="example@example.com", name="user example")

        chapter1 = Chapter(id="chapter1", book_id="book1", chapter_number=1, title="chapter 1")
        chapter2 = Chapter(id="chapter2", book_id="book2", chapter_number=2, title="chapter 2")
        chapter3 = Chapter(id="chapter3", book_id="book3", chapter_number=3, title="chapter 3")
        chapter4 = Chapter(id="chapter4", book_id="book4", chapter_number=1, title="chapter 1")
        chapter5 = Chapter(id="chapter5", book_id="book5", chapter_number=6, title="chapter 6")
        chapter6 = Chapter(id="chapter6", book_id="book6", chapter_number=10, title="chapter 10")
        chapter7 = Chapter(id="chapter7", book_id="book7", chapter_number=3, title="chapter 3")

        books = [
            Book(id="book1", owner_id="user", title="title1", genre="genre1", quotation_marks="ge", chapters=[chapter1]),
            Book(id="book2", owner_id="456", title="title2", genre="genre2", quotation_marks="fr", chapters=[chapter2]),
            Book(id="book3", owner_id="user", title="title3", genre="genre1", quotation_marks="ge", chapters=[chapter3]),
            Book(id="book4", owner_id="user", title="title4", genre="genre2", quotation_marks="fr", chapters=[chapter4]),
            Book(id="book5", owner_id="123", title="title5", genre="genre3", quotation_marks="ge", chapters=[chapter5]),
            Book(id="book6", owner_id="567", title="title6", genre="genre1", quotation_marks="ge", chapters=[chapter6]),
            Book(id="book7", owner_id="102", title="title7", genre="genre3", quotation_marks="ge", chapters=[chapter7]),
        ]
        mock_book_repository.list_books_for_owner.side_effect = (
            lambda owner_id: [b for b in books if b.owner_id == user.id]
        )

        query = GetUserBooksCommand(mock_book_repository)
        owner_id = "user"

        result = query.run(owner_id)

        mock_book_repository.list_books_for_owner.assert_called_once_with("user")

        assert isinstance(result, List)
        assert len(result) == 3
        assert result[0].id == "book1"
        assert result[1].title == "title3"
        assert result[2].genre == "genre2"