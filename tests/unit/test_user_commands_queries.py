import pytest
from unittest.mock import Mock

from app.application.commands.create_user import CreateUserCommand
from app.application.commands.delete_user import DeleteUserCommand
from app.application.commands.update_user import UpdateUserCommand
from app.application.dto.user_dto import CreateUserRequest, UserResponse, UpdateUserRequest
from app.domain.entities.user import User
from app.domain.ports.user_repository import UserRepository
from app.domain.errors import UserErrors

@pytest.fixture
def mock_user_repository():
    return Mock(spec=UserRepository)

class TestUserCommand:
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