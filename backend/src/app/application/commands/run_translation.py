from pathlib import Path
from app.application.dto.translation_dto import TranslateBookRequest, TranslateBookResponse
from app.domain.errors import BookErrors, FileErrors, TranslationTaskErrors
from app.domain.ports.book_repository import BookRepository
from app.domain.ports.file_repository import FileRepository
from app.domain.ports.translation_port import TranslationPort


class RunBookTranslationCommand:
    def __init__(
        self,
        book_repo: BookRepository,
        translation_port: TranslationPort,
        file_repo: FileRepository,
        base_dir: str,
    ):
        self.book_repo = book_repo
        self.translation_port = translation_port
        self.file_repo = file_repo
        self.base_dir = base_dir

    def run(self, dto: TranslateBookRequest) -> TranslateBookResponse:
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

        translated_chapters = 0

        for chapter in book.chapters:
            should_be_translated = dto.translate_all or (chapter.id in selected_ids)

            chapter_content = chapter.content
            chapter_text = chapter_content.text if chapter_content else ""

            footnotes_obj = chapter_content.footnotes if chapter_content else None
            footnotes_md = footnotes_obj.to_markdown() if footnotes_obj else ""

            if not should_be_translated:
                self._append_to_file(path=output_path, text=chapter_text, footnotes_md=footnotes_md)
                continue

            paragraphs = chapter_text.split("\n\n")
            translated_paragraphs = []

            for i in range(0, len(paragraphs), dto.batch_size):
                batch = paragraphs[i : i + dto.batch_size]

                if not any(p.strip() for p in batch):
                    translated_paragraphs.extend(batch)
                    continue

                draft = self.translation_port.translate_batch(paragraphs=batch, genre=book.genre)
                improved = self.translation_port.improve_batch(original_paragraphs=batch, draft_translations=draft, genre=book.genre)
                final = self.translation_port.apply_active_voice_batch(paragraphs=improved)

                translated_paragraphs.extend(final)

            final_text = "\n\n".join(translated_paragraphs)
            self._append_to_file(path=output_path, text=final_text, footnotes_md=footnotes_md)
            translated_chapters += 1

        book.mark_translated()

        return TranslateBookResponse(
            book_id=book.id,
            output_path=str(output_path),
            translated_chapters=translated_chapters,
            status=book.status.value,
        )

    def _append_to_file(self, path: Path, text: str, footnotes_md: str) -> None:
        body = text or ""
        if footnotes_md:
            body = f"{body}\n\n{footnotes_md}\n\n"
        else:
            body = f"{body}\n\n"

        with open(path, "a", encoding="utf-8") as f:
            f.write(body)

