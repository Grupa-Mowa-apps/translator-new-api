from dataclasses import dataclass
from typing import Optional
from app.domain.errors import UserErrors

@dataclass
class User:
    id: str
    email: str
    name: Optional[str] = None

    def change_email(self, new_email: str) -> None:
        if not new_email or not new_email.strip():
            raise ValueError(UserErrors.EMAIL_CANNOT_BE_EMPTY)
        self.email = new_email.strip()

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