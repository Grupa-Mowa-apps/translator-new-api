from sqlalchemy.orm import Session
from app.domain.entities.user import User
from app.domain.ports.user_repository import UserRepository
from app.infrastructure.db.models import UserDB
from app.domain.errors import UserErrors
from typing import Iterable, Optional

def _row_to_domain_user(user: UserDB) -> User:
    return User(id=user.id, email=user.email, name=user.name)

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, user: User) -> None:
        self.session.add(UserDB(id=user.id, email=user.email, name=user.name))
        self.session.commit()

    def get(self, user_id: str) -> Optional[User]:
        # [CODE REVIEW] [BLOCKER] Metoda get() powinna zwracać None gdy nie znajdzie użytkownika,
        # nie rzucać wyjątku. Obsługa błędów "not found" powinna być w warstwie application.
        user_row = self.session.get(UserDB, user_id)
        if not user_row:
            raise ValueError(UserErrors.USER_NOT_FOUND)
        return User(id=user_row.id, email=user_row.email, name=user_row.name)
    
    def get_by_email(self, email: str) -> Optional[User]:
        # [CODE REVIEW] [BLOCKER] get_by_email() powinno zwracać None gdy nie znajdzie.
        # W CreateUserCommand używasz: if self.repo.get_by_email(dto.email) - to nigdy nie zadziała
        # poprawnie, bo metoda rzuci wyjątek zamiast zwrócić None.
        user_row = self.session.query(UserDB).filter(UserDB.email == email).first()
        if not user_row:
            raise ValueError(UserErrors.USER_NOT_FOUND)
        return User(id=user_row.id, email=user_row.email, name=user_row.name)
    
    def update(self, user: User) -> None:
        user_row = self.session.get(UserDB, user.id)
        if not user_row:
            raise ValueError(UserErrors.USER_NOT_FOUND)
        user_row.email = user.email
        user_row.name = user.name
        self.session.commit()

    def delete(self, user_id: str) -> None:
        user_row = self.session.get(UserDB, user_id)
        if not user_row:
            raise ValueError(UserErrors.USER_NOT_FOUND)
        self.session.delete(user_row)
        self.session.commit()

    def list_paginated_filtered(self, limit: int, email_like: Optional[str]) -> Iterable[User]:
        q = self.session.query(UserDB)
        if email_like:
            q = q.filter(UserDB.email.ilike(f"%{email_like}%"))
        q = q.order_by(UserDB.email.asc()).limit(limit)
        return [_row_to_domain_user(user_row) for user_row in q.all()]