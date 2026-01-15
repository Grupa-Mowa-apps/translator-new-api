from pydantic import BaseModel, EmailStr
from typing import Optional, List

class CreateUserRequest(BaseModel):
    email: EmailStr
    name: Optional[str]

class UpdateUserRequest(BaseModel):
    email: EmailStr
    name: Optional[str]

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: Optional[str]

    @classmethod
    def from_entity(cls, user):
        return cls(id=user.id, email=user.email, name=user.name)
