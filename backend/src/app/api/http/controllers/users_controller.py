from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.application.dto.user_dto import UserResponse, CreateUserRequest, UpdateUserRequest
from app.application.dto.book_dto import BookResponse
from app.application.commands.create_user import CreateUserCommand
from app.application.commands.update_user import UpdateUserCommand
from app.application.commands.delete_user import DeleteUserCommand
from app.application.commands.get_user_books import GetUserBooksCommand
from app.application.queries.get_user import GetUserQuery
from app.application.queries.list_users import ListUsersQuery
from app.infrastructure.db.repositories.user_repo_sqlalchemy import SqlAlchemyUserRepository
from app.infrastructure.db.repositories.book_repo_sqlalchemy import SqlAlchemyBookRepository

from app.infrastructure.db.dependencies import get_db

router = APIRouter(prefix="/users", tags=["users"])

def user_repo(db: Session):
    return SqlAlchemyUserRepository(db)

def book_repo(db: Session):
    return SqlAlchemyBookRepository(db)

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(dto: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        return CreateUserCommand(user_repo(db)).run(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: str, db: Session=Depends(get_db)):
    try:
        return GetUserQuery(user_repo(db)).run(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@router.get("", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def list_users(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    email_like: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return ListUsersQuery(user_repo(db)).run(limit, offset, email_like)

@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: str, dto: UpdateUserRequest, db: Session=Depends(get_db)):
    try:
        return UpdateUserCommand(user_repo(db)).run(user_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Session=Depends(get_db)):
    try:
        DeleteUserCommand(user_repo(db)).run(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@router.get("/{user_id}/books", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
def list_user_books(user_id: str, db: Session = Depends(get_db)):
    return GetUserBooksCommand(book_repo(db)).run(user_id)