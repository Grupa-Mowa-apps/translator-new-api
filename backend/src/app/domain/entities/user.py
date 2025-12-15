from dataclasses import dataclass
from typing import Optional
from app.domain.errors import UserErrors

@dataclass
class User:
    id: str
    email: str
    name: Optional[str] = None

    # CODE REVIEW: Dodaj type hint dla new_email
    # BLOCKER: Brak type hint utrudnia wykrywanie błędów przez mypy
    def change_email(self, new_email: str) -> None:  # TODO: Dodano type hint
        # SUGGESTION: Rozważ walidację formatu email (regex lub Value Object)
        if not new_email or not new_email.strip():
            raise ValueError(UserErrors.EMAIL_CANNOT_BE_EMPTY)
        self.email = new_email.strip()

    # CODE REVIEW: Dodaj type hint i walidację None
    # BLOCKER: new_name.strip() rzuci AttributeError jeśli new_name = None
    def change_name(self, new_name: Optional[str]) -> None:  # TODO: Dodano type hint
        # CRITICAL FIX NEEDED: Dodaj walidację None przed strip()
        # if new_name is None:
        #     self.name = None
        #     return
        self.name = new_name.strip()  # BUG: Crash jeśli new_name = None!

    # NIT: Dodaj type hint dla spójności
    def __repr__(self) -> str:  # TODO: Dodano type hint
        cls = self.__class__.__name__
        return f"{cls}(id={self.id!r}, email={self.email!r}, name={self.name!r})"
    
    # NIT: Dodaj type hint dla spójności
    def __str__(self) -> str:  # TODO: Dodano type hint
        return f"User: {self.name or self.email}"