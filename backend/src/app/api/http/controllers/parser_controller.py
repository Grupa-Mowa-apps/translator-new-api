from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.infrastructure.db.dependencies import get_db
from app.infrastructure.db.repositories.annotation_set_repo_sqlalchemy import SqlAlchemyAnnotationSetRepository
from app.infrastructure.db.repositories.book_repo_sqlalchemy import SqlAlchemyBookRepository
from app.infrastructure.db.repositories.file_repo_sqlalchemy import SqlAlchemyFileRepository
from app.infrastructure.parsing.parser_adapter import ParserAdapter

from app.application.commands.export_quotes_footnotes import ExportQuotesFootnotesCommand
from app.application.commands.apply_excel_translations import ApplyExcelTranslationsCommand
from app.application.dto.parser_dto import (
    ExportParserRequest,
    ExportParserResponse,
    ApplyParserTranslationsRequest,
    ApplyParserTranslationsResponse,
)

router = APIRouter(prefix="/books", tags=["parser"])

def book_repo(db: Session):
    return SqlAlchemyBookRepository(session=db)

def file_repo(db: Session):
    return SqlAlchemyFileRepository(session=db)

def annotation_repo(db: Session):
    return SqlAlchemyAnnotationSetRepository(session=db)

def parser_port():
    return ParserAdapter(base_dir="/app/backend/storage")

@router.post(
    "/{book_id}/parser/export", 
    response_model=ExportParserResponse,
    status_code=status.HTTP_200_OK,
)
def export_parser(book_id: str, dto: ExportParserRequest, db: Session = Depends(get_db)):
    try:
        cmd = ExportQuotesFootnotesCommand(
            book_repo=book_repo(db),
            annotation_repo=annotation_repo(db),
            excel_port=parser_port(),
            file_repo=file_repo(db),
        )
        return cmd.run(book_id=book_id, dto=dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post(
    "/{book_id}/parser/apply", 
    response_model=ApplyParserTranslationsResponse,
    status_code=status.HTTP_200_OK,
)
def apply_parser(book_id: str, dto: ApplyParserTranslationsRequest, db: Session = Depends(get_db)):
    try:
        cmd = ApplyExcelTranslationsCommand(
            book_repo=book_repo(db),
            annotation_repo=annotation_repo(db),
            excel_port=parser_port(),
            file_repo=file_repo(db),
        )
        return cmd.run(book_id=book_id, dto=dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get(
    "/{book_id}/annotations",
    status_code=status.HTTP_200_OK,
)
def list_annotation_sets(book_id: str, db: Session = Depends(get_db)):
    rows = annotation_repo(db).list_for_book(book_id)
    return [
        {
            "id": a.id,
            "book_id": a.book_id,
            "file_path": a.file_path,
            "status": str(a.status),
            "version": a.version,
        }
        for a in rows
    ]

@router.get(
    "/{book_id}/annotations/{annotation_set_id}/download",
    status_code=status.HTTP_200_OK,
)
def download_annotation_set(book_id: str, annotation_set_id: str, db: Session = Depends(get_db)):
    try:
        annotation_set = annotation_repo(db).get(annotation_set_id)
        if annotation_set.book_id != book_id:
            raise ValueError("Annotation set does not belong to this book")

        file_path = Path(annotation_set.file_path)
        return FileResponse(
            path=str(file_path),
            filename=file_path.name,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))