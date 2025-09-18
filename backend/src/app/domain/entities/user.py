from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: str
    email: str   # na przyszlosc
    name: Optional[str] = None

    def change_email(self, new_email) -> None:
        if not new_email or not new_email.strip():
            raise ValueError(f"Email cannot be empty")
        self.title = new_email.strip()

    def change_name(self, new_name) -> None:
        self.name = new_name.strip()