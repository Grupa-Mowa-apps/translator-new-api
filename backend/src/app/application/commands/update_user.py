import logging
from app.domain.ports.user_repository import UserRepository
from app.application.dto.user_dto import UpdateUserRequest, UserResponse
from app.domain.errors import UserErrors

logger = logging.getLogger(__name__)

class UpdateUserCommand:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def execute(self, user_id: str, dto: UpdateUserRequest) -> UserResponse:
        logger.info(f"Updating user: {user_id}")
        u = self.repo.get(user_id)
        if not u:
            logger.warning(f"User not found: {user_id}")
            raise ValueError(UserErrors.USER_NOT_FOUND)
        if dto.email:
            u.change_email(dto.email)
        if dto.name:
            u.change_name(dto.name)
        self.repo.update(u)
        self.repo.session.commit()
        logger.info(f"User updated successfully: {user_id}")
        return UserResponse.from_entity(u)
