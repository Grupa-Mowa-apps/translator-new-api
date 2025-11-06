from app.domain.ports.user_repository import UserRepository
from app.application.dto.user_dto import UpdateUserRequest, UserResponse
from app.domain.errors import UserErrors

class UpdateUserCommand:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def run(self, user_id: str, dto: UpdateUserRequest) -> UserResponse:
        user = self.repo.get(user_id)
        if not user:
            raise ValueError(UserErrors.USER_NOT_FOUND)
        if dto.email:
            user.change_email(dto.email)
        if dto.name:
            user.change_name(dto.name)
        self.repo.update(user)
        return UserResponse(id=user.id, email=user.email, name=user.name)