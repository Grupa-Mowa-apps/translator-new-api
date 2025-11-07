import pytest
from sqlalchemy.orm.session import Session

from app.infrastructure.db.repositories.user_repo_sqlalchemy import SqlAlchemyUserRepository
from app.domain.entities.user import User
from app.domain.errors import UserErrors

@pytest.fixture
def user_repository(db_session: Session):
    return SqlAlchemyUserRepository(db_session)

class TestSqlAlchemyUserRepository:
    def test_add_and_get_user(self, user_repository):
        user = User(id="123", email="user@example.com", name="example user")

        user_repository.add(user)

        retrieved_user = user_repository.get("123")

        assert retrieved_user is not None
        assert retrieved_user.id == "123"
        assert retrieved_user.email == "user@example.com"
        assert retrieved_user.name == "example user"

    def test_get_nonexistent_user_raises_error(self, user_repository):
        with pytest.raises(ValueError) as e:
            user_repository.get("nonexistent-id")
        assert str(e.value) == UserErrors.USER_NOT_FOUND

    def test_get_by_email(self, user_repository):
        user = User(id="123", email="user@example.com", name="example user")
        user_repository.add(user)

        found_user = user_repository.get_by_email("user@example.com")

        assert found_user is not None
        assert found_user.id == "123"
        assert found_user.email == "user@example.com"

    def test_get_by_email_not_found(self, user_repository):
        with pytest.raises(ValueError) as e:
            user_repository.get_by_email("nonexistent@example.com")
        assert str(e.value) == UserErrors.USER_NOT_FOUND

    def test_update_user(self, user_repository):
        user = User(id="123", email="user@example.com", name="example user")
        user_repository.add(user)

        user.email = "new-email@example.com"
        user.name = "new name"
        user_repository.update(user)

        updated_user = user_repository.get("123")
        assert updated_user is not None
        assert updated_user.id == "123"
        assert updated_user.email == "new-email@example.com"
        assert updated_user.name == "new name"

    def test_update_nonexistent_user_raises_error(self, user_repository):
        user = User(id="123", email="user@example.com", name="example user")

        with pytest.raises(ValueError) as e:
            user_repository.update(user)
        assert str(e.value) == UserErrors.USER_NOT_FOUND

    def test_delete_user(self, user_repository):
        user = User(id="123", email="user@example.com", name="example user")
        user_repository.add(user)

        user_repository.delete("123")

        with pytest.raises(ValueError) as e:
            user_repository.get("123")
        assert str(e.value) == UserErrors.USER_NOT_FOUND

    def test_delete_nonexistent_user_raises_error(self, user_repository):
        with pytest.raises(ValueError) as e:
            user_repository.delete("nonexistant-id")
        assert str(e.value) == UserErrors.USER_NOT_FOUND

    def test_list_paginated_filtered_no_filter(self, user_repository):
        users = [
            User(id="user1", email="user1@email.com", name="user one"),
            User(id="user2", email="user2@email.com", name="user two"),
            User(id="user3", email="user3@email.com", name="user three"),
            User(id="user4", email="user4@email.com", name="user four"),
            User(id="user5", email="user5@email.com", name="user five")
        ]
        for user in users:
            user_repository.add(user)

        result1 = user_repository.list_paginated_filtered(limit=3, email_like=None)

        assert isinstance(result1, list)
        assert len(result1) == 3
        assert result1[0].email == "user1@email.com"

        result2 = user_repository.list_paginated_filtered(limit=10, email_like=None)

        assert isinstance(result2, list)
        assert len(result2) == len(users)

    def test_list_paginated_filtered_with_filter(self, user_repository):
        users = [
            User(id="user1", email="user1@email.com", name="user one"),
            User(id="user2", email="user2example@email.com", name="user two"),
            User(id="user3", email="user3@email.com", name="user three"),
            User(id="user4", email="user4example@email.com", name="user four"),
            User(id="user5", email="user5@email.com", name="user five")
        ]
        for user in users:
            user_repository.add(user)
        
        result = user_repository.list_paginated_filtered(limit=3, email_like="example")

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0].id == "user2"