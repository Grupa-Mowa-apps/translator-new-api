from dataclasses import dataclass
from typing import Optional
from domain.errors import UserErrors

@dataclass
class User:
    id: str
    email: str
    name: Optional[str] = None

    def change_email(self, new_email) -> None:
        if not new_email or not new_email.strip():
            raise ValueError(UserErrors.EMAIL_CANNOT_BE_EMPTY)
        self.email = new_email.strip()

    def change_name(self, new_name) -> None:
        self.name = new_name.strip()

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}(id={self.id!r}, email={self.email!r}, name={self.name!r})"
    
    def __str__(self):
        return f"User: {self.name or self.email}"