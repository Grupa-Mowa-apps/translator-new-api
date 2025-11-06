from app.domain.ports.user_repository import UserRepository
from app.application.dto.user_dto import UserResponse
from typing import List, Optional

class ListUsersQuery:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def run(self, limit: int, email_like: Optional[str]) -> List[UserResponse]:
        users = self.repo.list_paginated_filtered(limit, email_like)
        return [UserResponse(id=u.id, email=u.email, name=u.name) for u in users]