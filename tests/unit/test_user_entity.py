import pytest
from app.domain.entities.user import User
from app.domain.errors import UserErrors

def test_change_email_happy_path():
    user = User(id="1", email="a@b.com", name=None)
    user.change_email("  x@y.com  ")
    assert user.email == "x@y.com"

def test_change_email_empty_raises():
    user = User(id="1", email="a@b.com")
    with pytest.raises(ValueError) as exc:
        user.change_email("  ")
    assert str(exc.value) == UserErrors.EMAIL_CANNOT_BE_EMPTY

def test_change_name_strips():
    user = User(id="1", email="a@b.com", name=None)
    user.change_name("  Ala  ")
    assert user.name == "Ala"