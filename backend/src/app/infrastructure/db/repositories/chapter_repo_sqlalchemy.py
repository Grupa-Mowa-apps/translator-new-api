from typing import Iterable, Optional
from sqlalchemy.orm import Session
from sqlalchemy import delete, select
from app.domain.entities.chapter import Chapter
from app.domain.errors import ChapterErrors
from app.domain.ports.chapter_repository import ChapterRepository
from app.domain.value_objects.chapter_content import ChapterContent
from app.infrastructure.db.models import ChapterDB

def _content_to_db(content: Optional[ChapterContent]) -> Optional[str]:
    return None if content is None else content.text

def _db_to_content(text: Optional[str]) -> Optional[ChapterContent]:
    return None if text is None else ChapterContent(text=text, footnotes=None)

def _row_to_domain_chapter(row: ChapterDB) -> Chapter:
    return Chapter(
        id=row.id,
        book_id=row.book_id,
        chapter_number=row.chapter_number,
        title=row.title,
        parent_id=row.parent_id,
        content=_db_to_content(row.content),
    )

def _domain_to_row_chapter(chapter: Chapter) -> ChapterDB:
    return ChapterDB(
        id=chapter.id,
        book_id=chapter.book_id,
        parent_id=chapter.parent_id,
        chapter_number=chapter.chapter_number,
        title=chapter.title,
        content=_content_to_db(chapter.content),
    )

class SqlAlchemyChapterRepository(ChapterRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    def add(self, chapter: Chapter) -> None:
        self.session.add(_domain_to_row_chapter(chapter=chapter))

    def get(self, chapter_id: str) -> Optional[Chapter]:
        chapter_row = self.session.get(ChapterDB, chapter_id)
        if chapter_row is None:
            raise ValueError(ChapterErrors.CHAPTER_NOT_FOUND)
        return _row_to_domain_chapter(row=chapter_row)
    
    def delete_for_book(self, book_id: str) -> bool:
        result = self.session.execute(
            delete(ChapterDB).where(ChapterDB.book_id == book_id)
        )
        return bool(result.rowcount and result.rowcount > 0) 
    
    def add_many(self, chapters: Iterable[Chapter]) -> int:
        chapters_list = list(chapters)

        chapters_list.sort(key=lambda c: (c.parent_id is not None, c.chapter_number))

        self.session.add_all([_domain_to_row_chapter(chapter) for chapter in chapters_list])
        return len(chapters_list)
    
    def list_for_book(self, book_id: str) -> Iterable[Chapter]:
        query = (
            select(ChapterDB)
            .where(ChapterDB.book_id == book_id)
            .order_by(ChapterDB.chapter_number.asc())
        )
        chapter_rows = self.session.execute(query).scalars().all()
        return [_row_to_domain_chapter(row) for row in chapter_rows]