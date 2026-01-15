import logging
from app.domain.ports.user_repository import UserRepository
from app.domain.errors import UserErrors

logger = logging.getLogger(__name__)

class DeleteUserCommand:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def execute(self, user_id: str) -> None:
        logger.info(f"Deleting user: {user_id}")
        if not self.repo.get(user_id):
            logger.warning(f"User not found: {user_id}")
            raise ValueError(UserErrors.USER_NOT_FOUND)
        self.repo.delete(user_id)
        logger.info(f"User deleted successfully: {user_id}")