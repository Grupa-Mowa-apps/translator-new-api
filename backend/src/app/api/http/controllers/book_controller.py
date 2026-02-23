import asyncio
import json
import os
from pathlib import Path
import traceback
import uuid
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.application.commands.process_book import ProcessBookCommand
from app.application.dto.translation_dto import TranslateBookRequest
from app.application.queries.get_book_with_chapters import GetBookWithChaptersQuery
from app.domain.entities.translation_task import TranslationTask
from app.infrastructure.book.book_mapper_adapter import BookMapperAdapter
from app.infrastructure.db.dependencies import get_db
from app.infrastructure.db.repositories.book_repo_sqlalchemy import SqlAlchemyBookRepository
from app.infrastructure.db.repositories.chapter_repo_sqlalchemy import SqlAlchemyChapterRepository
from app.infrastructure.db.repositories.file_repo_sqlalchemy import SqlAlchemyFileRepository

from app.application.dto.book_dto import BookWithChaptersResponse, CreateBookRequest, BookResponse, ProcessBookRequest
from app.application.dto.chapter_dto import ChapterResponse
from app.application.commands.create_book_from_file import CreateBookFromFileCommand
from app.application.commands.delete_book import DeleteBookCommand
from app.application.queries.get_book import GetBookQuery
from app.application.queries.list_books import ListBooksForOwnerQuery
from app.infrastructure.db.repositories.translation_task_repo_sqlalchemy import SqlAlchemyTranslationTaskRepository
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.files.file_storage_adapter import FileStorageAdapter
from app.infrastructure.llm.llm_completion_adapter import LLMCompletionAdapter
from app.infrastructure.parsing.markdown_analyzer_adapter import MarkdownAnalyzerAdapter
from app.infrastructure.translation.translation_adapter import TranslationAdapter
from app.infrastructure.progress.progress_tracker_instance import progress_tracker

from app.setup.config.settings import FILE_STORAGE_DIR
from app.application.commands.run_translation_sync import RunBookTranslationSyncCommand
from app.application.commands.run_translation_async import RunBookTranslationAsyncCommand

import logging
logger = logging.getLogger("uvicorn.error")

router = APIRouter(prefix="/books", tags=["books"])


def book_repo(db: Session) -> SqlAlchemyBookRepository:
    return SqlAlchemyBookRepository(session=db)

def file_repo(db: Session) -> SqlAlchemyFileRepository:
    return SqlAlchemyFileRepository(session=db)

def chapter_repo(db: Session) -> SqlAlchemyChapterRepository:
    return SqlAlchemyChapterRepository(session=db)

def file_storage() -> FileStorageAdapter:
    return FileStorageAdapter()

def book_mapper() -> BookMapperAdapter:
    base_dir = Path(os.environ.get("FILE_STORAGE_DIR", "/app/backend/storage"))

    md_analyzer_factory = lambda rel_path: MarkdownAnalyzerAdapter(
        file_path=str((base_dir / rel_path).resolve())
    )
    return BookMapperAdapter(md_analyzer_factory=md_analyzer_factory)

def get_llm_port() -> LLMCompletionAdapter:
    return LLMCompletionAdapter()

def get_translation_port() -> TranslationAdapter:
    return TranslationAdapter(llm=get_llm_port())

def translation_task_repo(db: Session) -> SqlAlchemyTranslationTaskRepository:
    return SqlAlchemyTranslationTaskRepository(session=db)
    

@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(dto: CreateBookRequest, db: Session = Depends(get_db)):
    try:
        cmd = CreateBookFromFileCommand(
            book_repo=book_repo(db),
            file_repo=file_repo(db),
        )
        return cmd.execute(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
def get_book(book_id: str, db: Session = Depends(get_db)):
    try:
        return GetBookQuery(book_repo(db)).execute(book_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("", response_model=list[BookResponse], status_code=status.HTTP_200_OK)
def list_books(owner_id: str, db: Session = Depends(get_db)):
    try:
        return ListBooksForOwnerQuery(book_repo(db)).execute(owner_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post("/{book_id}/map", response_model=BookResponse, status_code=status.HTTP_200_OK)
def mapp_book(book_id: str, db: Session = Depends(get_db)):
    try:
        cmd = ProcessBookCommand(
            book_repo=book_repo(db),
            file_repo=file_repo(db),
            chapter_repo=chapter_repo(db),
            file_storage=file_storage(),
            book_mapper=book_mapper(),
        )
        return cmd.execute(dto=ProcessBookRequest(book_id=book_id))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/{book_id}/chapters", response_model=list[ChapterResponse], status_code=status.HTTP_200_OK)
def list_chapters(book_id: str, db: Session = Depends(get_db)):
    rows = list(chapter_repo(db).list_for_book(book_id))
    return [
        ChapterResponse(
            id=chapter.id,
            book_id=chapter.book_id,
            chapter_number=chapter.chapter_number,
            title=chapter.title,
            parent_id=chapter.parent_id,
            content=chapter.content.text,
        )
        for chapter in rows
    ]

@router.get("/{book_id}/full", response_model=BookWithChaptersResponse)
def get_book_full(book_id: str, db: Session = Depends(get_db)):
    try:
        query = GetBookWithChaptersQuery(
            book_repo=book_repo(db),
            chapter_repo=chapter_repo(db),
        )
        book = query.execute(book_id)

        return BookWithChaptersResponse(
            id=book.id,
            owner_id=book.owner_id,
            title=book.title,
            genre=book.genre,
            quotation_marks=book.quotation_marks,
            file_id=book.file_id,
            status=book.status.value,
            version=book.version,
            chapters=[
                ChapterResponse(
                    id=ch.id,
                    book_id=ch.book_id,
                    chapter_number=ch.chapter_number,
                    title=ch.title,
                    parent_id=ch.parent_id,
                    content=ch.content.text if ch.content else None,
                )
                for ch in book.chapters
            ],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: str, owner_id: str, db: Session = Depends(get_db)):
    try:
        cmd = DeleteBookCommand(book_repo(db))
        cmd.execute(book_id=book_id, owner_id=owner_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/{book_id}/translation/run-download", response_class=FileResponse, status_code=200)
async def run_translation_and_download_sync(
    book_id: str,
    dto: TranslateBookRequest,
    db: Session = Depends(get_db),
):
    try:
        cmd = RunBookTranslationSyncCommand(
            book_repo=book_repo(db),
            translation_port=get_translation_port(),
            file_repo=file_repo(db),
            base_dir=Path(FILE_STORAGE_DIR),
        )

        result = await cmd.run(dto=dto, task_id="sync")

        md_path = Path(result.output_path)
        if not md_path.exists():
            raise HTTPException(status_code=500, detail=f"Translated file not found: {md_path}")

        return FileResponse(path=str(md_path), filename=md_path.name, media_type="text/markdown")

    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        tb = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Translation failed: {e}\n\n{tb}")

@router.post("/{book_id}/translation/start", status_code=200)
async def start_translation_async(
    book_id: str,
    dto: TranslateBookRequest,
    db: Session = Depends(get_db),
):
    task_id = uuid.uuid4().hex

    task = TranslationTask(id=task_id, book_id=book_id)
    translation_task_repo(db).add(task)
    db.commit()

    async def _job():
        db2 = SessionLocal()
        try:
            cmd = RunBookTranslationAsyncCommand(
                book_repo=book_repo(db2),
                translation_port=get_translation_port(),
                file_repo=file_repo(db2),
                base_dir=Path(FILE_STORAGE_DIR),
                progress=progress_tracker,
                task_repo=translation_task_repo(db2),
            )
            await cmd.run(dto=dto, task_id=task_id)
            db2.commit()
        except Exception:
            db2.rollback()
        finally:
            db2.close()

    asyncio.create_task(_job())
    return {"task_id": task_id}


@router.get("/translation/progress/{task_id}")
async def translation_progress(task_id: str):
    if not progress_tracker.has_task(task_id=task_id):
        await progress_tracker.start(task_id=task_id)

    async def gen():
        queue = await progress_tracker.subscribe(task_id=task_id)
        try:
            while True:
                update = await queue.get()
                yield f"data: {json.dumps(update)}\n\n"
                msg = str(update.get("message", "")).strip().lower()
                if update.get("progress") == 100 or msg.startswith("failed") or msg.startswith("canceled") or msg.startswith("cancelled"):
                    break
        finally:
            await progress_tracker.unsubscribe(task_id=task_id, queue=queue)

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )

@router.get("/translation/download/{task_id}", response_class=FileResponse)
def download_translation(task_id: str, db: Session = Depends(get_db)):
    task = translation_task_repo(db).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if not task.output_path:
        raise HTTPException(status_code=500, detail="Task finished but output_path is missing")

    md_path = Path(task.output_path)
    if not md_path.exists():
        raise HTTPException(status_code=500, detail=f"Translated file not found: {md_path}")

    return FileResponse(
        path=str(md_path),
        filename=md_path.name,
        media_type="text/markdown",
    )
