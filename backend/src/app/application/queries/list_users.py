from app.domain.ports.user_repository import UserRepository
from app.application.dto.user_dto import UserResponse
from typing import List, Optional

class ListUsersQuery:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def execute(self, limit: int, offset: int, email_like: Optional[str]) -> List[UserResponse]:
        users = self.repo.list_paginated_filtered(limit, offset, email_like)
        return [UserResponse.from_entity(u) for u in users]