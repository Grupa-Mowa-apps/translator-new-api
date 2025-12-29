from pathlib import Path
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse

from app.infrastructure.parsing.parser_adapter import ParserAdapter
from app.domain.value_objects.quotation_marks import QuoteType

router = APIRouter(prefix="/parser", tags=["parser-dev"])

UPLOADS_DIR = Path("uploads")

def parser_port() -> ParserAdapter:
    return ParserAdapter(base_dir=UPLOADS_DIR)

def _quote_type_from_form(q: str) -> QuoteType:
    q = (q or "").strip().upper()
    if q == "FR":
        return QuoteType.FR
    if q in ("GE", "DE"):
        return QuoteType.GE
    raise ValueError("quote_type must be FR or GE")

@router.post("/export")
async def dev_export(
    md_file: UploadFile = File(...),
    quote_type: str = Form("FR"),
    excel_filename: str = Form("export.xlsx"),
):
    try:
        qt = _quote_type_from_form(quote_type)

        UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
        md_path = UPLOADS_DIR / md_file.filename
        md_path.write_bytes(await md_file.read())

        out_xlsx_path, stats = parser_port().export_from_markdown(
            md_path=str(md_path),
            quote_type=qt,
            excel_path=excel_filename,
        )

        return FileResponse(
            path=out_xlsx_path,
            filename=Path(out_xlsx_path).name,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"X-Parser-Stats": str(stats)},
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/apply")
async def dev_apply(
    md_file: UploadFile = File(...),
    excel_file: UploadFile = File(...),
    output_md_filename: str = Form("output_REPLACED.md"),
):
    try:
        UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

        md_path = UPLOADS_DIR / md_file.filename
        md_path.write_bytes(await md_file.read())

        xlsx_path = UPLOADS_DIR / excel_file.filename
        xlsx_path.write_bytes(await excel_file.read())

        out_md_path = parser_port().apply_translations_from_excel(
            excel_path=str(xlsx_path),
            md_input_path=str(md_path),
            md_output_path=output_md_filename,
        )

        return FileResponse(
            path=out_md_path,
            filename=Path(out_md_path).name,
            media_type="text/markdown",
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
