import uuid
import logging
from app.application.dto.user_dto import CreateUserRequest, UserResponse
from app.domain.entities.user import User
from app.domain.ports.user_repository import UserRepository
from app.domain.errors import UserErrors

logger = logging.getLogger(__name__)

class CreateUserCommand:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def execute(self, dto: CreateUserRequest) -> UserResponse:
        logger.info(f"Creating user with email: {dto.email}")
        if self.repo.get_by_email(dto.email):
            logger.warning(f"Email already in use: {dto.email}")
            raise ValueError(UserErrors.EMAIL_ALREADY_IN_USE)
        user = User(id=uuid.uuid4().hex, email=dto.email, name=dto.name)
        self.repo.add(user)
        logger.info(f"User created successfully: {user.id}")
        return UserResponse.from_entity(user)