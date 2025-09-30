import pytest
from app.domain.entities.user import User
from app.domain.errors import UserErrors

def test_change_email_happy_path():
    u = User(id="1", email="a@b.com", name=None)
    u.change_email("  x@y.com  ")
    assert u.email == "x@y.com"

def test_change_email_empty_raises():
    u = User(id="1", email="a@b.com")
    with pytest.raises(ValueError) as exc:
        u.change_email("  ")
    assert str(exc.value) == UserErrors.EMAIL_CANNOT_BE_EMPTY

def test_change_name_strips():
    u = User(id="1", email="a@b.com", name=None)
    u.change_name("  Ala  ")
    assert u.name == "Ala"