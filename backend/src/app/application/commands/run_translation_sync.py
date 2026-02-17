from app.domain.ports.progress_tracker_port import ProgressTrackerPort
from app.infrastructure.progress.null_progress_tracker import NullProgressTracker
from app.application.commands.abstract_run_translation import BaseRunBookTranslationCommand
from app.application.dto.translation_dto import TranslateBookRequest

class RunBookTranslationSyncCommand(BaseRunBookTranslationCommand):

    async def _on_start(self, task_id: str, dto: TranslateBookRequest) -> None:
        return

    async def _on_progress(self, task_id: str, progress: int, message: str, translated_chapters: int) -> None:
        return

    async def _on_complete(self, task_id: str, output_path: str) -> None:
        return

    async def _on_fail(self, task_id: str, error: Exception) -> None:
        return
