from pathlib import Path
from app.domain.entities.translation_task import TranslationTask
from app.domain.ports.progress_tracker_port import ProgressTrackerPort
from app.domain.ports.translation_task_repository import TranslationTaskRepository
from app.application.commands.abstract_run_translation import BaseRunBookTranslationCommand
from app.application.dto.translation_dto import TranslateBookRequest
from app.domain.ports.book_repository import BookRepository
from app.domain.ports.file_repository import FileRepository
from app.domain.ports.translation_port import TranslationPort

class RunBookTranslationAsyncCommand(BaseRunBookTranslationCommand):
    def __init__(
        self,
        book_repo: BookRepository,
        translation_port: TranslationPort,
        file_repo: FileRepository,
        base_dir: Path,
        progress: ProgressTrackerPort,
        task_repo: TranslationTaskRepository,
    ):
        super().__init__(book_repo, translation_port, file_repo, base_dir)
        self.progress = progress
        self.task_repo = task_repo

    async def _on_start(self, task_id: str, dto: TranslateBookRequest) -> None:
        await self.progress.start(task_id=task_id, initial_message="Started")

        task = self.task_repo.get(task_id)
        if not task:
            raise ValueError("TranslationTask not found")

        task.start_translation_task()
        task.message = "Translation started"
        self.task_repo.update(task)

    async def _on_set_total(self, task_id: str, total: int) -> None:
        task = self.task_repo.get(task_id)
        if task:
            task.total_chapters = total
            self.task_repo.update(task)

    async def _on_progress(self, task_id: str, progress: int, message: str, translated_chapters: int) -> None:
        task = self.task_repo.get(task_id)
        if task:
            task.update_progress(percent=progress, msg=message, translated_chapters=translated_chapters)
            self.task_repo.update(task)

        await self.progress.update(task_id=task_id, progress=progress, message=message)

    async def _on_complete(self, task_id: str, output_path: str) -> None:
        task = self.task_repo.get(task_id)
        if task:
            task.output_path = output_path
            task.complete_task("Translation completed")
            self.task_repo.update(task)

        await self.progress.complete(task_id=task_id, message="Translation completed")

    async def _on_fail(self, task_id: str, error: Exception) -> None:
        task = self.task_repo.get(task_id)
        if task:
            task.fail(msg=f"Failed: {error}")
            self.task_repo.update(task)

        await self.progress.fail(task_id=task_id, message=f"Failed: {error}")
