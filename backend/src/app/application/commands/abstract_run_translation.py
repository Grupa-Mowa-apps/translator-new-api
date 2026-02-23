import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from app.application.dto.translation_dto import TranslateBookRequest, TranslateBookResponse
from app.domain.errors import BookErrors, FileErrors, TranslationTaskErrors
from app.domain.ports.book_repository import BookRepository
from app.domain.ports.file_repository import FileRepository
from app.domain.ports.translation_port import TranslationPort


@dataclass
class _ProgressState:
    total: int
    done: int = 0
    translated_chapters: int = 0

    def percent(self) -> int:
        if self.total <= 0:
            return 0
        return int(self.done / self.total * 100)


class BaseRunBookTranslationCommand(ABC):

    def __init__(
        self,
        book_repo: BookRepository,
        translation_port: TranslationPort,
        file_repo: FileRepository,
        base_dir: Path,
    ):
        self.book_repo = book_repo
        self.translation_port = translation_port
        self.file_repo = file_repo
        self.base_dir = base_dir

    async def run(self, dto: TranslateBookRequest, task_id: str) -> TranslateBookResponse:
        try:
            await self._on_start(task_id=task_id, dto=dto)

            if dto.batch_size <= 0:
                raise ValueError(TranslationTaskErrors.INVALID_BATCH_SIZE)

            if not dto.translate_all and not dto.chapter_ids:
                raise ValueError(TranslationTaskErrors.INVALID_TRANSALTION_CHOICE)

            selected_ids = set(dto.chapter_ids or [])

            book = self.book_repo.get(book_id=dto.book_id)
            if not book:
                raise ValueError(BookErrors.BOOK_NOT_FOUND)

            if not book.file_id:
                raise ValueError(FileErrors.FILE_NOT_FOUND)

            file = self.file_repo.get(file_id=book.file_id)
            if not file:
                raise ValueError(FileErrors.FILE_NOT_FOUND)

            book.start_translation()
            self.book_repo.update(book=book)

            out_dir = self.base_dir / "translations"
            out_dir.mkdir(parents=True, exist_ok=True)

            output_name = dto.output_filename or f"{Path(file.path).stem}_translated.md"
            output_path = out_dir / output_name
            if output_path.suffix.lower() != ".md":
                output_path = output_path.with_suffix(".md")

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text("", encoding="utf-8")

            chapters_to_translate = [
                ch for ch in book.chapters
                if dto.translate_all or (ch.id in selected_ids)
            ]
            total = max(1, len(chapters_to_translate))
            state = _ProgressState(total=total)

            await self._on_set_total(task_id=task_id, total=total)

            for chapter in book.chapters:
                should_translate = dto.translate_all or (chapter.id in selected_ids)

                chapter_content = chapter.content
                chapter_text = chapter_content.text if chapter_content else ""

                if getattr(chapter, "title", None):
                    chapter_text = f"## {chapter.title}\n\n{chapter_text}"

                footnotes_obj = chapter_content.footnotes if chapter_content else None
                footnotes_md = footnotes_obj.to_markdown() if footnotes_obj else ""

                if not chapter_text.strip() and not footnotes_md.strip():
                    continue

                chapter_header = ""

                if not should_translate:
                    await asyncio.to_thread(
                        self._append_to_file,
                        output_path,
                        chapter_header + chapter_text,
                        footnotes_md,
                    )
                    continue

                paragraphs = chapter_text.split("\n\n")
                translated_paragraphs: list[str] = []

                for i in range(0, len(paragraphs), dto.batch_size):
                    batch = paragraphs[i : i + dto.batch_size]

                    if not any(p.strip() for p in batch):
                        translated_paragraphs.extend(batch)
                        continue

                    draft = self.translation_port.translate_batch(paragraphs=batch, genre=book.genre)
                    improved = self.translation_port.improve_batch(
                        original_paragraphs=batch,
                        draft_translations=draft,
                        genre=book.genre,
                    )
                    final = self.translation_port.apply_active_voice_batch(paragraphs=improved)
                    translated_paragraphs.extend(final)

                final_text = "\n\n".join(translated_paragraphs)
                await asyncio.to_thread(self._append_to_file, output_path, final_text, footnotes_md)

                state.translated_chapters += 1
                state.done += 1

                await self._on_progress(
                    task_id=task_id,
                    progress=state.percent(),
                    message=f"Translated chapter {state.done}/{state.total}",
                    translated_chapters=state.translated_chapters,
                )

            book.mark_translated()
            self.book_repo.update(book=book)

            await self._on_complete(task_id=task_id, output_path=str(output_path))

            return TranslateBookResponse(
                book_id=book.id,
                output_path=str(output_path),
                translated_chapters=state.translated_chapters,
                status=book.status.value,
            )

        except Exception as e:
            await self._on_fail(task_id=task_id, error=e)
            raise

    # ---------- extension points ----------

    @abstractmethod
    async def _on_start(self, task_id: str, dto: TranslateBookRequest) -> None:
        print("SYNC COMMAND RUNNING")
        return

    async def _on_set_total(self, task_id: str, total: int) -> None:
        return

    @abstractmethod
    async def _on_progress(self, task_id: str, progress: int, message: str, translated_chapters: int) -> None: ...

    @abstractmethod
    async def _on_complete(self, task_id: str, output_path: str) -> None: ...

    @abstractmethod
    async def _on_fail(self, task_id: str, error: Exception) -> None: ...

    # ---------- helper ----------

    def _append_to_file(self, path: Path, text: str, footnotes_md: str) -> None:
        body = text or ""
        if footnotes_md:
            body = f"{body}\n\n{footnotes_md}\n\n"
        else:
            body = f"{body}\n\n"

        with open(path, "a", encoding="utf-8") as f:
            f.write(body)
