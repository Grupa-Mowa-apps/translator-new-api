import uuid
from app.application.dto.user_dto import CreateUserRequest, UserResponse
from app.domain.entities.user import User
from app.domain.ports.user_repository import UserRepository
from app.domain.errors import UserErrors

class CreateUserCommand:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def run(self, dto: CreateUserRequest) -> UserResponse:
        if self.repo.get_by_email(dto.email):
            raise ValueError(UserErrors.EMAIL_ALREADY_IN_USE)
        user = User(id=uuid.uuid4().hex, email=dto.email, name=dto.name)
        self.repo.add(user)
        return UserResponse(id=user.id, email=user.email, name=user.name)