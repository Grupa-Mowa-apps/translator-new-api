from typing import Iterable, Optional
from sqlalchemy.orm import Session
from app.domain.entities.user import User
from app.domain.ports.user_repository import UserRepository
from app.infrastructure.db.models import UserDB

def _row_to_domain_user(user: UserDB) -> User:
    return User(id=user.id, email=user.email, name=user.name)

class SqlAlchemyUserRepository(UserRepository):
    session: Session
    
    def __init__(self, session: Session):
        self.session = session

    def add(self, user: User) -> None:
        self.session.add(UserDB(id=user.id, email=user.email, name=user.name))

    def get(self, user_id: str) -> Optional[User]:
        user_row = self.session.get(UserDB, user_id)
        if not user_row:
            return None
        return _row_to_domain_user(user_row)
    
    def get_by_email(self, email: str) -> Optional[User]:
        user_row = self.session.query(UserDB).filter(UserDB.email == email).first()
        if not user_row:
            return None
        return _row_to_domain_user(user_row)
    
    def update(self, user: User) -> bool:
        user_row = self.session.get(UserDB, user.id)
        if user_row is None:
            return False
        user_row.email = user.email
        user_row.name = user.name
        return True

    def delete(self, user_id: str) -> bool:
        user_row = self.session.get(UserDB, user_id)
        if user_row is None:
            return False
        self.session.delete(user_row)
        return True

    def list_paginated_filtered(self, limit: int, offset: int, email_like: Optional[str]) -> Iterable[User]:
        q = self.session.query(UserDB)
        if email_like:
            q = q.filter(UserDB.email.ilike(f"%{email_like}%"))
        q = q.order_by(UserDB.email.asc()).offset(offset).limit(limit)
        return [_row_to_domain_user(user_row) for user_row in q.all()]