from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dto.chapter_dto import ChapterResponse
from app.infrastructure.db.dependencies import get_db
from app.infrastructure.db.repositories.chapter_repo_sqlalchemy import SqlAlchemyChapterRepository


router = APIRouter(prefix="/chapters", tags=["chapters"])

def chapter_repo(db: Session) -> SqlAlchemyChapterRepository:
    return SqlAlchemyChapterRepository(session=db)

@router.get("/{chapter_id}", response_model=ChapterResponse, status_code=status.HTTP_200_OK)
def get_chapter(chapter_id: str, db: Session = Depends(get_db)):
    chapter = chapter_repo(db).get(chapter_id=chapter_id)
    if not chapter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")
    
    return ChapterResponse(
        id=chapter.id,
        book_id=chapter.book_id,
        chapter_number=chapter.chapter_number,
        title=chapter.title,
        parent_id=chapter.parent_id,
        content=chapter.content.text,
    )