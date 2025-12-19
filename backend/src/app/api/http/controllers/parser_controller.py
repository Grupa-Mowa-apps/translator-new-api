from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.db.dependencies import get_db
from app.infrastructure.db.repositories.book_repo_sqlalchemy import SqlAlchemyBookRepository
from app.infrastructure.parsing.markdown_analyzer_adapter import MarkdownAnalyzerAdapter
from app.infrastructure.parsing.parser_adapter import ParserAdapter

from app.application.commands.export_quotes_footnotes import ExportQuotesFootnotesCommand
from app.application.commands.apply_excel_translations import ApplyExcelTranslationsCommand
from app.application.dto.parser_dto import (
    ExportParserRequest, ExportParserResponse,
    ApplyParserTranslationsRequest, ApplyParserTranslationsResponse,
)

router = APIRouter(prefix="/books", tags=["books-parser"])

def book_repo(db: Session):
    return SqlAlchemyBookRepository(db)

def parser_port():
    return ParserAdapter(base_dir="uploads")

@router.post("/{book_id}/parser/export", response_model=ExportParserResponse)
def export_parser(book_id: str, dto: ExportParserRequest, db: Session = Depends(get_db)):
    try:
        cmd = ExportQuotesFootnotesCommand(book_repo(db), parser_port())
        return cmd.run(book_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{book_id}/parser/apply", response_model=ApplyParserTranslationsResponse)
def apply_parser(book_id: str, dto: ApplyParserTranslationsRequest, db: Session = Depends(get_db)):
    try:
        cmd = ApplyExcelTranslationsCommand(book_repo(db), parser_port())
        return cmd.run(book_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
