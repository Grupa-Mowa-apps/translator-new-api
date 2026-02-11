from typing import Optional
from sqlalchemy.orm import Session

from app.domain.entities.translation_task import TranslationTask
from app.domain.ports.translation_task_repository import TranslationTaskRepository
from app.domain.value_objects.translation_status import TranslationStatus

from app.infrastructure.db.models import TranslationTaskDB


def _row_to_domain_task(row: TranslationTaskDB) -> TranslationTask:
    return TranslationTask(
        id=row.id,
        book_id=row.book_id,
        total_chapters=row.total_chapters,
        message=row.message,
        output_path=row.output_path,
        status=TranslationStatus(row.status),
        progress=row.progress,
        translated_chapters=row.translated_chapters,
    )


class SqlAlchemyTranslationTaskRepository(TranslationTaskRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    def add(self, task: TranslationTask) -> None:
        self.session.add(
            TranslationTaskDB(
                id=task.id,
                book_id=task.book_id,
                status=task.status.value,
                progress=task.progress,
                translated_chapters=task.translated_chapters,
                total_chapters=task.total_chapters,
                message=task.message,
                output_path=task.output_path,
            )
        )

    def get(self, task_id: str) -> Optional[TranslationTask]:
        row = self.session.get(TranslationTaskDB, task_id)
        if row is None:
            return None
        return _row_to_domain_task(row)

    def update(self, task: TranslationTask) -> bool:
        row = self.session.get(TranslationTaskDB, task.id)
        if row is None:
            return False

        row.book_id = task.book_id
        row.status = task.status.value
        row.progress = task.progress
        row.translated_chapters = task.translated_chapters
        row.total_chapters = task.total_chapters
        row.message = task.message
        row.output_path = task.output_path

        return True
