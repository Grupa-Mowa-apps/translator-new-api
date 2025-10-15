from app.domain.ports.user_repository import UserRepository
from app.domain.errors import UserErrors

class DeleteUserCommand:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def run(self, user_id: str) -> None:
        if not self.repo.get(user_id):
            raise ValueError(UserErrors.USER_NOT_FOUND)
        self.repo.delete(user_id)