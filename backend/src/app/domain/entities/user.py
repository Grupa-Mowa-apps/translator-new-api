from dataclasses import dataclass
from typing import Optional
import re
from app.domain.errors import UserErrors

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

@dataclass
class User:
    id: str
    email: str
    name: Optional[str] = None

    def __post_init__(self) -> None:
        if not re.match(EMAIL_REGEX, self.email):
            raise ValueError(UserErrors.INVALID_EMAIL_FORMAT)

    def change_email(self, new_email: str) -> None:
        email = new_email.strip()
        if not email:
            raise ValueError(UserErrors.EMAIL_CANNOT_BE_EMPTY)
        if not re.match(EMAIL_REGEX, email):
            raise ValueError(UserErrors.INVALID_EMAIL_FORMAT)
        self.email = email

    def change_name(self, new_name: Optional[str]) -> None:
        if new_name is None:
            self.name = None
            return
        self.name = new_name.strip()

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}(id={self.id!r}, email={self.email!r}, name={self.name!r})"
    
    def __str__(self) -> str:
        return f"User: {self.name or self.email}"