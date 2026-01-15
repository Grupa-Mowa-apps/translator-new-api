from app.domain.ports.user_repository import UserRepository
from app.domain.errors import UserErrors
from app.application.dto.user_dto import UserResponse
from typing import Optional

class GetUserQuery:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def execute(self, user_id: str) -> Optional[UserResponse]:
        user = self.repo.get(user_id)
        if not user:
            raise ValueError(UserErrors.USER_NOT_FOUND)
        return UserResponse.from_entity(user)