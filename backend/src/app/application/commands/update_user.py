from app.domain.ports.user_repository import UserRepository
from app.application.dto.user_dto import UpdateUserRequest, UserResponse
from app.domain.errors import UserErrors

class UpdateUserCommand:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def run(self, user_id: str, dto: UpdateUserRequest) -> UserResponse:
        u = self.repo.get(user_id)
        if not u:
            raise ValueError(UserErrors.USER_NOT_FOUND)
        if not dto.email:
            u.change_email(dto.email)
        if not dto.name:
            u.change_name(dto.name)
        self.repo.update(u)
        return UserResponse(id=u.id, email=u.email, name=u.name)