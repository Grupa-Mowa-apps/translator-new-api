from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.application.commands.upload_translated_excel import UploadTranslatedExcelCommand
from app.domain.ports.annotation_set_repository import AnnotationSetRepository
from app.domain.ports.book_repository import BookRepository
from app.domain.ports.excel_quotes_footnotes import ExcelQuotesFootnotesPort
from app.domain.ports.file_repository import FileRepository
from app.infrastructure.db.dependencies import get_db
from app.infrastructure.db.repositories.annotation_set_repo_sqlalchemy import SqlAlchemyAnnotationSetRepository
from app.infrastructure.db.repositories.book_repo_sqlalchemy import SqlAlchemyBookRepository
from app.infrastructure.db.repositories.file_repo_sqlalchemy import SqlAlchemyFileRepository
from app.infrastructure.files.file_storage_adapter import FileStorageAdapter
from app.infrastructure.parsing.parser_adapter import ParserAdapter

from app.application.commands.export_quotes_footnotes import ExportQuotesFootnotesCommand
from app.application.commands.apply_excel_translations import ApplyExcelTranslationsCommand
from app.application.dto.parser_dto import (
    ExportParserRequest,
    ExportParserResponse,
    ApplyParserTranslationsRequest,
    ApplyParserTranslationsResponse,
    UploadTranslatedExcelRequest,
    UploadTranslatedExcelResponse,
)

router = APIRouter(prefix="/books", tags=["parser"])

def get_book_repo(db: Session = Depends(get_db)) -> BookRepository:
    return SqlAlchemyBookRepository(session=db)

def get_file_repo(db: Session = Depends(get_db)):
    return SqlAlchemyFileRepository(session=db)

def get_file_storage() -> FileStorageAdapter:
    return FileStorageAdapter()

def get_annotation_repo(db: Session = Depends(get_db)) -> AnnotationSetRepository:
    return SqlAlchemyAnnotationSetRepository(session=db)

def get_parser_port() -> ExcelQuotesFootnotesPort:
    return ParserAdapter(base_dir="/app/backend/storage")

def get_export_cmd(
    book_repo: BookRepository = Depends(get_book_repo),
    annotation_repo: AnnotationSetRepository = Depends(get_annotation_repo),
    excel_port: ExcelQuotesFootnotesPort = Depends(get_parser_port),
    file_repo: FileRepository = Depends(get_file_repo)
) -> ExportQuotesFootnotesCommand:
    return ExportQuotesFootnotesCommand(
        book_repo=book_repo,
        annotation_repo=annotation_repo,
        excel_port=excel_port,
        file_repo=file_repo,
    )

@router.post(
    "/{book_id}/parser/export", 
    response_model=ExportParserResponse,
    status_code=status.HTTP_200_OK,
)
def export_parser(book_id: str, dto: ExportParserRequest, db: Session = Depends(get_db)):
    try:
        cmd = ExportQuotesFootnotesCommand(
            book_repo=get_book_repo(db),
            annotation_repo=get_annotation_repo(db),
            excel_port=get_parser_port(),
            file_repo=get_file_repo(db),
        )
        return cmd.execute(book_id=book_id, dto=dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get(
    "/{book_id}/annotations/{annotation_set_id}/download",
    status_code=status.HTTP_200_OK,
)
def download_annotation_set(book_id: str, annotation_set_id: str, db: Session = Depends(get_db)):
    try:
        annotation_set = get_annotation_repo(db).get(annotation_set_id)
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

# @router.post(
#     "/{book_id}/parser/apply",
#     response_model=ApplyParserTranslationsResponse,
#     status_code=status.HTTP_200_OK,
# )
# def apply_parser(book_id: str, dto: ApplyParserTranslationsRequest, db: Session = Depends(get_db)):
#     try:
#         cmd = ApplyExcelTranslationsCommand(
#             book_repo=get_book_repo(db),
#             annotation_repo=get_annotation_repo(db),
#             excel_port=get_parser_port(),
#             file_repo=get_file_repo(db),
#         )
#         return cmd.run(book_id=book_id, dto=dto)
#     except ValueError as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post(
    "/{book_id}/parser/apply",
    response_model=ApplyParserTranslationsResponse,
    status_code=status.HTTP_200_OK,
)
def apply_parser(book_id: str, dto: ApplyParserTranslationsRequest, db: Session = Depends(get_db)):
    try:
        cmd = ApplyExcelTranslationsCommand(
            book_repo=get_book_repo(db),
            annotation_repo=get_annotation_repo(db),
            excel_port=get_parser_port(),
            file_repo=get_file_repo(db),
        )
        return cmd.execute(book_id=book_id, dto=dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get(
    "/{book_id}/annotations",
    status_code=status.HTTP_200_OK,
)
def list_annotation_sets(book_id: str, db: Session = Depends(get_db)):
    rows = get_annotation_repo(db).list_for_book(book_id)
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
    "/{book_id}/download-with-translated-annotations",
    status_code=status.HTTP_200_OK,
)
def download_book_with_translated_annotations(book_id: str, db: Session = Depends(get_db)):
    try:
        book = get_book_repo(db).get(book_id)
        if not book or book.status.value != "annotations_applied":
            raise ValueError("Book annotations not applied")
        
        file = get_file_repo(db).get(file_id=book.file_id)
        md_path = Path(file.path)
        
        return FileResponse(
            path=str(md_path),
            filename=md_path.name,
            media_type="text/markdown",
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.post(
    "/{book_id}/parser/export-download",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
)
def export_parser_and_download(
    book_id: str,
    dto: ExportParserRequest,
    cmd: ExportQuotesFootnotesCommand = Depends(get_export_cmd),
):
    try:
        result = cmd.execute(book_id=book_id, dto=dto)
        xlsx_path = Path(result.excel_path)

        if not xlsx_path.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Exported file not found on disk: {xlsx_path}",
            )
        
        headers = {
            "X-Footnotes-Count": str(result.footnotes_count),
            "X-Quotes-Count": str(result.quotes_count),
            "X-Blockquotes-Count": str(result.blockquotes_count),
        }

        return FileResponse(
            path=str(xlsx_path),
            filename=xlsx_path.name,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers=headers,
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{book_id}/parser/upload-translated",
    response_model=UploadTranslatedExcelResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_translated_excel(
    book_id: str,
    excel_file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        content = await excel_file.read()

        cmd = UploadTranslatedExcelCommand(
            book_repo=get_book_repo(db),
            annotation_repo=get_annotation_repo(db),
            file_storage=get_file_storage(),
        )

        return cmd.execute(
            dto=UploadTranslatedExcelRequest(
                book_id=book_id,
                filename=excel_file.filename or "translated_excel.xlsx",
                content=content,
                content_type=excel_file.content_type,
            )
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
